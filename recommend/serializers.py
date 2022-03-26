from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer
# from .models import Book, LargeCategory, MediumCategory, SmallCategory
from .models import Book, SmallCategory

from rest_framework import serializers


class BookCRUDSerializer(ModelSerializer):


    class Meta:
        model = Book
        fields = ['name','ISBN', 'author','image', 'score', 'publisher', 'category']



class CategoryCRUDSerializer(ModelSerializer):


    class Meta:
        model = SmallCategory
        fields = '__all__'










class BookSerializer(ModelSerializer):
    # method_name=None
    category = SerializerMethodField()

    # instance : book
    # The method name defaults to `get_{field_name}`.
    # tree 구조

    # 없으면 11 query, 1.69ms
    # 있으면 20 query , 2.51ms
    def get_category(self, instance):
        small_category = instance.category

        medium_category = small_category.category

        if medium_category is None:
            return f"{small_category.name}"
        large_category = medium_category.category
        if large_category is None:
            return f"{medium_category.name} / {small_category.name}"
        return f"{large_category.name} / {medium_category.name} / {small_category.name}"

    class Meta:
        model = Book
        fields = ['name', 'author','category','image', 'score', 'publisher']






# 모델 시리얼라이즈 xx
# id만 받아서 그냥 시리얼라이즈 커스텀
# ModelSerializer : 모델에 대한 것




class BookSelectSerializer(Serializer):
    # id = serializers.Field()


    # PrimaryKeyRelatedField may be used to represent the target of the relationship using its primary key.
    # By default this field is read-write, although you can change this behavior using the read_only flag.
    # pk를 사용하여 관계된 대상을 나타냄
    # 필드가 to many relationship을 나타내는 데 사용되는 경우 many=True 속성이 필요
    # ids = PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Book.objects.all()
    # )

    ids = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=100))

    class Meta:
        # model = Book
        fields = ['ids'] # ids ->
