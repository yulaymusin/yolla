from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import F
from forumcorona.topic.models import Topic


class ListViewContextPaginated:
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by

        limited_page_range = 0
        for i in context['paginator'].page_range:
            limited_page_range = i
        context['limited_page_range'] = range(1, 100) if limited_page_range >= 100 else context['paginator'].page_range
        context['last_page'] = limited_page_range if limited_page_range >= 100 else 0
        return context

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            try:
                paginate_by = int(self.request.GET.get('paginate_by'))
                # It is better if user can't choose too big number, unless DB work slowly
                if paginate_by <= 100:
                    self.paginate_by = paginate_by
            except ValueError:
                pass
        return super().get_paginate_by(queryset)


class MsgInFormValid:
    success_message = ''

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class SuperUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser is False:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff is False:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TopicsCategoriesContext:
    # ForNewUpdateInArticleJumbotron

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topics_values = Topic.objects.all().values('id', 'en_name', category_en_name=F('category_id__en_name'))
        topics_categories = {}
        for topic in topics_values:
            topics_categories[topic['category_en_name']] = {}
        for topic in topics_values:
            topics_categories[topic['category_en_name']][topic['id']] = topic['en_name']

        context['topics_categories'] = topics_categories
        return context
