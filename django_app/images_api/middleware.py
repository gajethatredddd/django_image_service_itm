import time
import json
import logging
from datetime import datetime
from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2

logger = logging.getLogger('images_api.middleware')

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        ip = self._get_client_ip(request)
        geo = self._get_geo(ip)

        request_info = {
            "method": request.method,
            "path": request.get_full_path(),
            "query_params": request.GET.dict(),
            "headers": dict(request.headers),
            "remote_addr": self._get_client_ip(request),
            "body": self._get_request_body(request),
            "geo": geo,
        }
        cache_hit = False
        cache_key = None
        if request.method == "GET":
            try:
                from django.utils.cache import _generate_cache_key
                cache_key = _generate_cache_key(request, key_prefix="views.decorators.cache.cache_page")
                if cache_key and cache.get(cache_key):
                    cache_hit = True
            except Exception:
                pass

        response = self.get_response(request)

        duration = time.time() - start_time
        response_info = {
            "status_code": response.status_code,
            "content_length": len(response.content) if hasattr(response, "content") else 0,
            "duration_ms": round(duration * 1000, 2),
            "cache_hit": cache_hit,
            "cache_key": cache_key,
        }

        log_data = {
            "timestamp": str(datetime.now()),
            "request": request_info,
            "user": {
                "id": getattr(request.user, "id", None),
                "username": getattr(request.user, "username", None),
                "authenticated": request.user.is_authenticated,
                "groups": [g.name for g in request.user.groups.all()] if request.user.is_authenticated else [],
            },
            "response": response_info,
        }

        logger.info(json.dumps(log_data, ensure_ascii=False, indent=2))

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def _get_request_body(self, request):
        try:
            body = request.body.decode("utf-8")
            if body:
                try:
                    return json.loads(body)
                except Exception:
                    return body
        except Exception:
            return None

    def _get_geo(self, ip):
        try:
            g = GeoIP2()
            return {
                "country": g.country(ip)['country_name'],
                "city": g.city(ip)['city'],
            }
        except Exception:
            return {"country": None, "city": None}