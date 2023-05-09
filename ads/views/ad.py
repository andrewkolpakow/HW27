import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from users.models import User
from django.core.paginator import Paginator

from ads.models import Category, Ad



# class AdListCreateView(View):
#
#     def get(self, request):
#         all_ads = Ad.objects.all()
#         return JsonResponse([ad.serialize() for ad in all_ads], safe=False)
#
#     def post(self, request):
#         data = json.loads(request.body)
#         new_ad = Ad.objects.create(**data)
#         return JsonResponse(new_ad.serialize(), safe = False)

TOTAL_ON_PAGE = 5
@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    queryset = Ad.objects.order_by("-price")
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        ads_on_page = paginator.get_page(page_number)


        return JsonResponse({
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "items": [ad.serialize() for ad in ads_on_page]
        }, safe=False)

@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, pk=data.pop("author"))
        category = get_object_or_404(Category, pk=data.pop("category"))

        new_ad = Ad.objects.create(author=author, category=category, **data)
        return JsonResponse(new_ad.serialize())


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())


    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_category = Category.objects.create(**data)
        return JsonResponse(new_category.serialize())

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView (UpdateView):
    model = Ad
    fields = "__all__"
    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "name" in data:
            self.object.name = data.get("name")
        if "price" in data:
            self.object.price = data.get("price")
        if "author_id" in data:
            author = get_object_or_404(User, pk=data.get("author_id"))
            self.object.author = author
        if "category" in data:
            category = get_object_or_404(Category, name=data.get("category"))
            self.object.category = category

        return JsonResponse(self.object.serialize())

@method_decorator(csrf_exempt, name="dispatch")

class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView (UpdateView):
    model = Ad
    fields = "__all__"
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse(self.object.serialize())
