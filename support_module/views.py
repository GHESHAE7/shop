from django.shortcuts import render
from django.views.generic.base import View
from .models import SupportCategory
from django.http import HttpResponse, HttpRequest
from django.db.models import Q


class SupportView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        search = self.request.GET.get("search") or None
        categories_support = (
            SupportCategory.objects.filter(is_active=True, supports__isnull=False)
            .prefetch_related("supports")
            .distinct()
        )
        if search is not None:
            categories_support = categories_support.filter(
                Q(supports__name__icontains=search)
                | Q(supports__description__icontains=search)
                | Q(name__icontains=search)
            )
        context = {
            "categories_support": categories_support,
        }
        return render(request, "support_module/support.html", context)
