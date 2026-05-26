from django.core.paginator import Paginator

from .constants import DEFAULT_PAGE_SIZE


def paginate_queryset(request, queryset):
    paginator = Paginator(queryset, DEFAULT_PAGE_SIZE)
    return paginator.get_page(request.GET.get("page"))
