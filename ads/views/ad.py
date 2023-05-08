import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView

from ads.models import Category, Ad



class AdListCreateView(View):

    def get(self, request):
        all_ads = Ad.objects.all()
        return JsonResponse([ad.serialize() for ad in all_ads], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(**data)
        return JsonResponse(new_ad.serialize(), safe = False)

class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())

