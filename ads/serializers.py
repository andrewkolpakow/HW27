import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category
from users.models import User
from users.serializers import UserListSerializer, LocationSerializer


class UserAdSerializer(ModelSerializer):
    locations = LocationSerializer(many=True)
    age_of_born = SerializerMethodField()

    def get_age_of_born(self, obj):
        return datetime.date.today().year - obj.age


    class Meta:
        model = User
        fields = ["locations", "username", "age_of_born"]


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdListSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ["name", "price"]


class AdDetailSerializer(ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_filed="name", queryset=Category.objects.all())


    class Meta:
        model = Ad
        fields = "__all__"
