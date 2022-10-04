import os
import zipfile
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from yolla.common.utils import lang, get_hash_md5
from . import models as m


FILE_MAX_SIZE = 10000000  # 10 million bytes, 10 000 KB, 10 MB
ALLOWED_FILENAME_EXTENSIONS = (
    'csv', 'numbers', 'ods', 'wk3', 'wks', 'xls', 'xlsb', 'xlsx',  # spreadsheet
    'acsm', 'apnx', 'azw', 'azw3', 'cbr', 'cbt', 'cbz', 'epub', 'fb2', 'ibooks', 'kfx', 'lit', 'lrf', 'mbp', 'mobi', 'opf', 'prc', 'tcr',
    'vbk',  # e-book
    '3dm', '3ds', 'dwg', 'dxf', 'max', 'obj', 'stp',  # computer-aided design/drafting
    'art', 'arw', 'avif', 'bmp', 'cr2', 'crw', 'dcm', 'dds', 'djvu', 'dng', 'exr', 'flif', 'fpx', 'gif', 'hdr', 'heic', 'ithmb', 'jp2',
    'jpeg', 'jpg', 'jxr', 'kdc', 'mac', 'nef', 'nrw', 'orf', 'pcd', 'pct', 'pcx', 'pef', 'pgm', 'pict', 'pictclipping', 'plist', 'png',
    'psd', 'pspimage', 'raf', 'raw', 'rwl', 'sfw', 'sr2', 'tga', 'thm', 'tif', 'tiff', 'wbmp', 'webp', 'xcf', 'yuv',  # raster graphics
    'flipchart', 'key', 'odp', 'pps', 'ppsx', 'ppt', 'pptx',  # presentation
    'adoc', 'afpub', 'chm', 'csk', 'doc', 'docx', 'dot', 'dotx', 'eml', 'fdxt', 'hwp', 'log', 'm3u', 'msg', 'odm', 'odt','oxps', 'pages',
    'pdf', 'pmd', 'pub', 'rtf', 'shs', 'sxw', 'tex', 'txt', 'vmg', 'vnt', 'wp5', 'wpd', 'wps', 'xml', 'xps',  # office document and text
    '264', '3g2', '3gp', '3gpp', 'aep', 'amv', 'arf', 'asf', 'avi', 'bik', 'braw', 'camproj', 'camrec', 'ced', 'cmproj', 'cmrec', 'cpi',
    'dav', 'dir', 'divx', 'dvsd', 'esp3', 'f4v', 'flv', 'g64', 'h264', 'ifo', 'imoviemobile', 'm2ts', 'm4v', 'mepx', 'mkv', 'mod', 'modd',
    'mov', 'mp4', 'mpeg', 'mpg', 'mproj', 'mse', 'mswmm', 'mts', 'mxf', 'nfv', 'ogv', 'osp', 'pds', 'pz', 'qt', 'rcproject', 'rm', 'rmvb',
    'srt', 'swf', 'thp', 'trec', 'ts', 'tvs', 'veg', 'vep', 'vob', 'vpj', 'vproj', 'vro', 'webm', 'wlmp', 'wmv', 'xesc',  # video
    'ai', 'cdr', 'cvs', 'emf', 'emz', 'eps', 'gvdesign', 'mix', 'odg', 'otg', 'pd', 'std', 'svg', 'svgz', 'vsd', 'wmf',
    'wpg',  # vector graphics
    '3ga', '4mp', 'aa', 'aac', 'aax', 'adpcm', 'aif', 'aifc', 'aiff', 'aimppl', 'amr', 'ape', 'asx', 'au', 'aup', 'awb', 'caf', 'cda',
    'cdo', 'flac', 'flp', 'gsm', 'iff', 'kar', 'koz', 'm3u8', 'm4a', 'm4b', 'm4p', 'm4r', 'mid', 'midi', 'mmf', 'mp2', 'mp3', 'mpa', 'mpc',
    'mpga', 'mui', 'nfa', 'oga', 'ogg', 'oma', 'opus', 'qcp', 'ra', 'ram', 'rta', 'vqf', 'wav', 'wma', 'xspf',  # audio
)
MAX_TOTAL_ATTACHMENT = 10


@login_required
def attach_documents(request, opinion_pk):
    if request.method == 'POST' and request.FILES:
        opinion_values = get_object_or_404(
            m.Opinion.objects.values('status'),
            pk=opinion_pk, publisher=request.user
        )
        if opinion_values['status'] not in (4, 5):
            raise PermissionDenied

        documents = request.FILES.getlist('documents[]')
        documents_md5 = []
        for document in documents:
            if document.size >= FILE_MAX_SIZE:
                raise PermissionDenied  # Error. Size limit.
            if document.name.lower().split('.')[-1] not in ALLOWED_FILENAME_EXTENSIONS:
                raise PermissionDenied  # Error. Forbidden file type.
            documents_md5.append(get_hash_md5(document.file.name))

        before_attached = m.OpinionAttachment.objects.filter(opinion_id=opinion_pk, deleted=False).values_list('md5', flat=True)
        if len(documents) + len(before_attached) > MAX_TOTAL_ATTACHMENT:
            raise PermissionDenied  # Error. Too many files.

        existing_attachment_values = m.OpinionAttachment.objects.filter(md5__in=documents_md5).values('document', 'md5')
        existing_documents = {}
        for attached_md5 in existing_attachment_values:
            existing_documents[attached_md5['md5']] = attached_md5['document']

        new_objects = []
        for document in documents:
            md5 = get_hash_md5(document.file.name)
            if md5 in before_attached:
                continue
            new_objects.append(m.OpinionAttachment(
                opinion_id=opinion_pk,
                document=existing_documents[md5] if md5 in existing_documents else document,
                original_label=document.name,
                md5=md5,
                size=document.size,
            ))
        m.OpinionAttachment.objects.bulk_create(new_objects)

        attachment_values = m.OpinionAttachment.objects.filter(opinion_id=opinion_pk, deleted=False)\
            .values('id', 'document', 'original_label', 'size')
        documents_list = []
        for document in attachment_values:
            documents_list.append({
                'url': settings.MEDIA_URL + document['document'], 'name': document['original_label'], 'size': document['size'],
                'delete_url': reverse_lazy('opinion:delete_document', kwargs={'attachment_pk': document['id']}),
            })
        return JsonResponse(documents_list, safe=False)

    opinion_values = get_object_or_404(
        m.Opinion.objects.values(
            'recorded', 'status',
            publisher_name=F('publisher_id__name'),
            topic_category_apex_name=F('topic_id__category_id__apex_id__' + lang('_name')),
            topic_category_name=F('topic_id__category_id__' + lang('_name')),
            topic_name=F('topic_id__' + lang('_name')),
            apex_recorded=F('apex_id__recorded'),
            apex_publisher_name=F('apex_id__publisher_id__name'),
            apex_text=F('apex_id__' + lang('_text')),
            text=F(lang('_text')),
        ),
        pk=opinion_pk, publisher=request.user
    )
    if opinion_values['status'] not in (4, 5):
        raise PermissionDenied
    return render(request, 'opinion/attach_documents.html', {
        'label': _('Documents of your reply'),
        'opinion': opinion_values,
        'documents': m.OpinionAttachment.objects.filter(opinion_id=opinion_pk, deleted=False).values('id', 'document', 'original_label', 'size'),
        'file_max_size': FILE_MAX_SIZE,
        'allowed_filename_extensions': ALLOWED_FILENAME_EXTENSIONS,
        'max_total_documents': MAX_TOTAL_ATTACHMENT,
    })


@login_required
def delete_document(request, attachment_pk):
    if request.method == 'POST':
        attachment_values = get_object_or_404(
            m.OpinionAttachment.objects.values('opinion_id', opinion_publisher_id=F('opinion_id__publisher_id')),
            pk=attachment_pk, deleted=False
        )
        if attachment_values['opinion_publisher_id'] != request.user.id:
            raise PermissionDenied
        m.OpinionAttachment.objects.filter(pk=attachment_pk).update(deleted=True)
        messages.info(request, _('Document deleted.'))
        return redirect(reverse_lazy('opinion:attach_documents', kwargs={'opinion_pk': attachment_values['opinion_id']}))

    attachment_values = get_object_or_404(
        m.OpinionAttachment.objects.values('opinion_id', 'document', 'original_label', 'size'),
        pk=attachment_pk, deleted=False
    )
    return render(request, 'opinion/delete_document.html', {
        'label': _('Delete document'),
        'document': attachment_values,
    })


def zip_documents(request, opinion_pk):
    opinion_values = get_object_or_404(
        m.Opinion.objects.values(
            'recorded',
            publisher_name=F('publisher_id__name'),
            topic_category_en_name=F('topic_id__category_id__en_name'),
            topic_en_name=F('topic_id__en_name'),
        ),
        pk=opinion_pk
    )

    zip_path = os.path.join(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT), 'zip')
    if not os.path.exists(zip_path):
        os.makedirs(zip_path)
    zip_filename = '{topic_category_en_name} — {topic_en_name} — {publisher_name} — {recorded}'.format(
        topic_category_en_name=opinion_values['topic_category_en_name'], topic_en_name=opinion_values['topic_en_name'],
        publisher_name=opinion_values['publisher_name'], recorded=opinion_values['recorded'].strftime("%Y-%m-%d %H-%M UTC")
    )
    zip_filename += '.zip'
    zip_path = os.path.join(zip_path, zip_filename)

    if not os.path.isfile(zip_path):
        attachment_values = m.OpinionAttachment.objects.filter(opinion_id=opinion_pk, deleted=False).values('document', 'original_label')
        if attachment_values:
            try:
                fz = zipfile.ZipFile(zip_path, 'w')  # Making the ZIP archive
                try:
                    for attachment in attachment_values:
                        file_path = os.path.join(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT), attachment['document'])
                        fz.write(file_path, arcname=attachment['original_label'])
                finally:
                    fz.close()
            except IOError:
                pass
        else:
            raise Http404
    return redirect(settings.MEDIA_URL + 'zip/' + zip_filename)
