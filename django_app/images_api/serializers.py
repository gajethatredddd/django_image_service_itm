from images_api.models import Image
from rest_framework import serializers
from PIL import Image as PILImage
import pytesseract

class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "name", "path", "size", "date", "extracted_text")
        read_only_fields = ("extracted_text",)

    def create(self, validated_data):
        image_instance = super().create(validated_data)
        try:
            text = self._extract_text(image_instance.path.path)
            image_instance.extracted_text = text
            image_instance.save()
        except Exception as e:
            print(f"OCR error: {e}")

        return image_instance

    def _extract_text(self, image_path):
        img = PILImage.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng+rus')
        return text
