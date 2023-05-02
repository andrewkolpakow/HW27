from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"status": "ok"}, status=200)

class CategoryListView(View):
    def get(self, request):
        all_categories = Category.objects.all()
        return JsonResponse([cat.serialize() for cat in all_categories], safe=False)

class AdListView(View):
    def get(self, request):
        all_ads = Ad.objects.all()
        return JsonResponse([ad.serialize() for ad in all_ads], safe=False)