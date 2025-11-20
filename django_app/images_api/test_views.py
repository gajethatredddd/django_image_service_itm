import tempfile
import pytest
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from images_api.models import Image

MEDIA_ROOT = tempfile.mkdtemp()


@pytest.mark.django_db
class TestImageViews:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="12345")

        self.client.force_authenticate(user=self.user)

        self.client.login(username="tester", password="12345")

    def test_image_list_view(self):
        url = reverse('images_api:image_list')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_image_upload_view_get(self):
        url = reverse('images_api:image_upload')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_image_upload_view_post(self):
        url = reverse('images_api:image_upload')

        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            img = PILImage.new('RGB', (1, 1), color='white')
            img.save(tmp, format='PNG')
            tmp.seek(0)
            image_file = SimpleUploadedFile("test.png", tmp.read(), content_type="image/png")

        with override_settings(MEDIA_ROOT=MEDIA_ROOT):
            response = self.client.post(url, {"name": "Uploaded Image", "path": image_file}, format='multipart')

        assert response.status_code in (200, 302)
        assert Image.objects.filter(name="Uploaded Image").exists()

    def test_image_delete_view(self):
        image = Image.objects.create(
            name="DeleteMe",
            path=SimpleUploadedFile("del.png", b"fake", content_type="image/png")
        )
        url = reverse('images_api:image_delete', args=[image.id])
        response = self.client.post(url)
        assert response.status_code in (302, 200)
        assert not Image.objects.filter(id=image.id).exists()

    def test_image_delete_ajax_view(self):
        image = Image.objects.create(
            name="ToDeleteAJAX",
            path=SimpleUploadedFile("ajax.png", b"fake", content_type="image/png")
        )
        url = reverse('images_api:image_delete_ajax', args=[image.id])
        response = self.client.post(url, {"_method": "DELETE"}, format='multipart')
        assert response.status_code == 200
        assert not Image.objects.filter(id=image.id).exists()

    def test_api_list(self):
        url = '/api/v1/lol/'
        response = self.client.get(url)
        assert response.status_code == 200

    def test_api_create(self):
        url = '/api/v1/lol/'

        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            img = PILImage.new('RGB', (1, 1), color='white')
            img.save(tmp, format='PNG')
            tmp.seek(0)
            image_file = SimpleUploadedFile("test_api.png", tmp.read(), content_type="image/png")

        with override_settings(MEDIA_ROOT=MEDIA_ROOT):
            response = self.client.post(url, {"name": "API Upload", "path": image_file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert Image.objects.filter(name="API Upload").exists()

    def test_api_detail(self):
        image = Image.objects.create(
            name="DetailTest",
            path=SimpleUploadedFile("detail.png", b"fake", content_type="image/png")
        )
        url = f'/api/v1/lol/{image.id}/'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['id'] == image.id

    def test_api_patch(self):
        image = Image.objects.create(
            name="PatchTest",
            path=SimpleUploadedFile("patch.png", b"fake", content_type="image/png")
        )
        url = f'/api/v1/lol/{image.id}/'
        response = self.client.patch(url, {"name": "Updated Name"}, format='json')
        assert response.status_code in (200, 202)
        image.refresh_from_db()
        assert image.name == "Updated Name"

    def test_api_delete(self):
        image = Image.objects.create(
            name="DeleteAPI",
            path=SimpleUploadedFile("delapi.png", b"fake", content_type="image/png")
        )
        url = f'/api/v1/lol/{image.id}/'
        response = self.client.delete(url)
        assert response.status_code in (204, 200)
        assert not Image.objects.filter(id=image.id).exists()

def test_wsgi_import():
    import image_service.wsgi
    assert hasattr(image_service.wsgi, 'application')


def test_asgi_import():
    import image_service.asgi
    assert hasattr(image_service.asgi, 'application')


def test_urls_resolves():
    url = reverse('images_api:image_list')
    resolver = resolve(url)
    assert resolver
