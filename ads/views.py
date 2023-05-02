import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"status": "ok"}, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class CategoryListCreateView(View):
    def get(self, request):
        all_categories = Category.objects.all()
        return JsonResponse([cat.serialize() for cat in all_categories], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_category = Category.objects.create(**data)
        return JsonResponse(new_category.serialize(), safe = False)


class AdListCreateView(View):
    def get(self, request):
        all_ads = Ad.objects.all()
        return JsonResponse([ad.serialize() for ad in all_ads], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(**data)
        return JsonResponse(new_ad.serialize(), safe = False)