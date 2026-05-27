from django.core.paginator import Paginator

from .constants import DEFAULT_PAGE_SIZE


def paginate_queryset(request, queryset, per_page=DEFAULT_PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))
