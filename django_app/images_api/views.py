import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Image
from .forms import ImageUploadForm

logger = logging.getLogger(__name__)

def image_list(request):
    images = Image.objects.all().order_by('-date')
    logger.info(f"Displaying list of {images.count()} images.")
    return render(request, 'images_api/image_list.html', {'images': images})

def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            logger.info(f"Image uploaded successfully: {new_image.name} (ID: {new_image.id})")
            return redirect('images_api:image_list')
        else:
            logger.warning("Image upload form is invalid.")
    else:
        form = ImageUploadForm()
    return render(request, 'images_api/image_upload.html', {'form': form})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    logger.info(f"Displaying detail for image: {image.name} (ID: {image.pk})")
    return render(request, 'images_api/image_detail.html', {'image': image})

def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image_name = image.name
    if request.method == 'POST':
        image.delete()
        logger.info(f"Image deleted successfully: {image_name} (ID: {pk})")
        return redirect('images_api:image_list')
    return redirect('images_api:image_list')

def image_delete_ajax(request, pk):
    if request.method == 'DELETE' or request.POST.get('_method') == 'DELETE':
        image = get_object_or_404(Image, pk=pk)
        image_name = image.name
        image.delete()
        logger.info(f"Image deleted via AJAX: {image_name} (ID: {pk})")
        return JsonResponse({'success': True, 'message': 'Image deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid method.'}, status=400)
