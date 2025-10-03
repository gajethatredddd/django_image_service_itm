from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Image
import os

class ImageTests(TestCase):
    def setUp(self):
        self.client = Client()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded_file = SimpleUploadedFile(
            'test.gif', small_gif, content_type='image/gif'
        )

    def test_image_creation(self):
        image = Image.objects.create(
            name='Test Image',
            path=self.uploaded_file
        )
        self.assertEqual(image.name, 'Test Image')
        self.assertTrue(image.size > 0)

    def test_image_upload_view(self):
        response = self.client.get(reverse('images_api:image_upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload')

    def test_image_list_view(self):
        response = self.client.get(reverse('images_api:image_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Images')

    def tearDown(self):
        for image in Image.objects.all():
            if os.path.isfile(image.path.path):
                os.remove(image.path.path)


