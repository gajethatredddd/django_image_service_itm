import logging
import json
import time
from datetime import datetime
from PIL import Image as PILImage, ImageOps
import pytesseract
from rest_framework import parsers, permissions
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Image
from .forms import ImageUploadForm
from .serializers import MySerializer

logger = logging.getLogger('images_api.middleware')

def image_list(request):
    images = Image.objects.all().order_by('-date')
    logger.info(f"Показано {images.count()} фото.")
    return render(request, 'images_api/image_list.html', {'images': images})

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            new_image.refresh_from_db()

            try:
                img_path = new_image.path.path
                img = PILImage.open(img_path)
                img = ImageOps.grayscale(img)
                img = img.point(lambda x: 0 if x < 128 else 255, '1')
                extracted_text = pytesseract.image_to_string(img, lang='eng+rus').strip()
                new_image.extracted_text = extracted_text
                new_image.save(update_fields=['extracted_text'])
                logger.info(f"Фото загружено: {new_image.name} (ID: {new_image.id})")
                logger.info(f"Извлечённый текст: {extracted_text}")
            except Exception as e:
                logger.warning(f"OCR не сработал для {new_image.name} (ID: {new_image.id}): {e}")

            return redirect('images_api:image_list')
        else:
            logger.warning("Ошибка загрузки изображения")
            return render(request, 'images_api/image_upload.html', {'form': form})
    else:
        form = ImageUploadForm()
    return render(request, 'images_api/image_upload.html', {'form': form})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    logger.info(f"Детали фото: {image.name} (ID: {image.pk})")
    return render(request, 'images_api/image_detail.html', {'image': image})

def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image_name = image.name
    if request.method == 'POST':
        image.delete()
        logger.info(f"Удалена: {image_name} (ID: {pk})")
        return redirect('images_api:image_list')
    return redirect('images_api:image_list')

def image_delete_ajax(request, pk):
    if request.method == 'DELETE' or request.POST.get('_method') == 'DELETE':
        image = get_object_or_404(Image, pk=pk)
        image_name = image.name
        image.delete()
        logger.info(f"Удалено через AJAX: {image_name} (ID: {pk})")
        return JsonResponse({'success': True, 'message': 'Image deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid method.'}, status=400)

@api_view(['GET'])
def available_ids(request):
    """Получить все существующие ID"""
    ids = Image.objects.values_list('id', flat=True).order_by('id')
    return Response({
        'available_ids': list(ids)
    })

@method_decorator(cache_page(30), name='dispatch')
class NewViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = MySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info("Redis работает")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_instance = serializer.save()
        image_instance.refresh_from_db()

        try:
            img_path = image_instance.path.path
            img = PILImage.open(img_path)
            extracted_text = pytesseract.image_to_string(img, lang='eng+rus')
            image_instance.extracted_text = extracted_text
            image_instance.save(update_fields=['extracted_text'])
            logger.info(f"OCR выполнен: {image_instance.name} (ID: {image_instance.id})")
        except Exception as e:
            logger.warning(f"OCR не сработал для {image_instance.name} (ID: {image_instance.id}): {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
