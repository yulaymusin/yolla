import os
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from forumcorona.common.utils import get_hash_md5, login_and_superuser_required
from . import models as m


FILE_MAX_SIZE = 1000000  # 1 million bytes, 1000 KB, 1 MB
ALLOWED_FILENAME_EXTENSIONS = ('jpeg', 'jpg', 'png', 'webp')


@login_and_superuser_required
def upload_images(request):
    if request.method == 'POST' and request.FILES:
        images = request.FILES.getlist('images[]')
        images_md5 = []
        for image in images:
            if image.size >= FILE_MAX_SIZE:
                raise PermissionDenied  # Error. Size limit.
            if image.name.lower().split('.')[-1] not in ALLOWED_FILENAME_EXTENSIONS:
                raise PermissionDenied  # Error. Forbidden file type.
            images_md5.append(get_hash_md5(image.file.name))

        before_uploaded = m.ArticleMedia.objects.all().values_list('md5', flat=True)

        existing_media_values = m.ArticleMedia.objects.filter(md5__in=images_md5).values('image', 'md5')
        existing_images = {}
        for uploaded_md5 in existing_media_values:
            existing_images[uploaded_md5['md5']] = uploaded_md5['image']

        new_objects = []
        for image in images:
            md5 = get_hash_md5(image.file.name)
            if md5 in before_uploaded:
                continue
            new_objects.append(m.ArticleMedia(
                image=existing_images[md5] if md5 in existing_images else image,
                md5=md5,
                size=image.size,
            ))
        m.ArticleMedia.objects.bulk_create(new_objects)

        media_values = m.ArticleMedia.objects.all().values('id', 'image', 'size')
        images_list = []
        for image in media_values:
            images_list.append({
                'id': image['id'], 'url': settings.MEDIA_URL + image['image'], 'name': image['image'].split('/')[-1],
                'size': image['size'], 'del_url': reverse_lazy('article:delete_image', kwargs={'media_pk': image['id']}),
                'path': '[MEDIA_URL]' + image['image'],
            })
        return JsonResponse(images_list, safe=False)

    return render(request, 'article/upload_images.html', {
        'label': 'Upload images',
        'images': [{'id': mf['id'], 'image': mf['image'], 'size': mf['size'], 'label': mf['image'].split('/')[-1]}
                   for mf in m.ArticleMedia.objects.all().values('id', 'image', 'size')],
        'file_max_size': FILE_MAX_SIZE,
        'allowed_filename_extensions': ALLOWED_FILENAME_EXTENSIONS,
    })


@login_and_superuser_required
def delete_image(request, media_pk):
    if request.method == 'POST':
        media_values = get_object_or_404(
            m.ArticleMedia.objects.values('image'),
            pk=media_pk
        )
        m.ArticleMedia.objects.filter(pk=media_pk).delete()
        image_path = os.path.join(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT), media_values['image'])
        if not os.path.isfile(image_path):
            messages.warning(request, 'The file does not exist.')
        else:
            os.remove(image_path)
        messages.info(request, 'Image deleted.')
        return redirect(reverse_lazy('article:upload_images') + '?list=1' if request.GET.get('list') == '1' else '')

    media_values = get_object_or_404(
        m.ArticleMedia.objects.values('image', 'size'),
        pk=media_pk
    )
    return render(request, 'article/delete_image.html', {
        'label': 'Delete image',
        'image': {'image': media_values['image'], 'size': media_values['size'], 'label': media_values['image'].split('/')[-1]},
    })
