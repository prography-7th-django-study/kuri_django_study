from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Book, SmallCategory
from .serializers import BookSerializer, BookSelectSerializer, BookCRUDSerializer, CategoryCRUDSerializer

# Book 등록 -> CRUD all --> modelviewset
class BookCRUD(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookCRUDSerializer

class CategoryCRUD(viewsets.ModelViewSet):
    queryset = SmallCategory.objects.all()
    serializer_class = CategoryCRUDSerializer


class BookListGenericAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # [{"id":1}, {"id":2}]

    # ## put로 하나 더 만듬 (view)
    # def patch(self, request):
    #     objects = list(request.data)
    #
    #     for o in objects:
    #         bookId = o['id']
    #         obj = self.queryset.get(id=bookId)
    #         obj.users.add(request.user.id)
    #
    #         # 상태코드 : 301(permanent) 302...
    #         # 선호도 표현 -- 상태 메소드 put, put에 대한 성공은 200대, response 200 --> 302
    #         # redirect xxxx
    #         # response 객체
    #     return redirect('books')


class BookListSelectGenericAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSelectSerializer
    http_method_names = ['patch']

    # permission_classes = [IsAuthenticated]

    # UpdateModelMixin
    def patch(self, request, *args, **kwargs):

        # partial = kwargs.pop('partial', True)
        # serializer = self.get_serializer(data=request.data, partial=partial)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.data['ids']
        for book_id in ids:
            obj = self.queryset.get(id=book_id)
            obj.users.add(request.user.id)

            # 상태코드 : 301(permanent) 302...
            # 선호도 표현 -- 상태 메소드 put, put에 대한 성공은 200대, response 200 --> 302
            # redirect xxxx
            # response 객체
        # Return the serializer instance that should be used for validating and
        # deserializing input, and for serializing output.

        return Response(serializer.data)







class BookListFavoriteGenericAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsAuthenticated]

    # 선택한 책 중에 작가, 대,중,소 분류, 출판사가 있으면 가중치를 줌
    # 그리고 가장 높은 가중치의 상위 3개만 띄워줌
#     def get_queryset(self):
#         ## 20 query, 3.45ms
#         # qs = super().get_queryset()
#
#         ## 11 query, 2.13ms
#         qs = super().get_queryset()
# #
# # """
# # 		0.11
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_smallcategory" WHERE "recommend_smallcategory"."id" = '10' LIMIT 21
# #  28 similar queries.  Duplicated 2 times.		0.24
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_smallcategory" WHERE "recommend_smallcategory"."id" = '8' LIMIT 21
# #  28 similar queries.  Duplicated 4 times.		0.08
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_smallcategory" WHERE "recommend_smallcategory"."id" = '8' LIMIT 21
# #  28 similar queries.  Duplicated 4 times.
# #
# #         ....`
# # """
#
#
#         # 32 query, 5.93ms
#         # selected_book = qs.filter(users=self.request.user)
#         #
#         # publishers = [x.publisher for x in selected_book]
#         # authors = [x.author for x in selected_book]
#         # large_categories = [x.category.name for x in selected_book]
#         # medium_categories = [x.category.category.name for x in selected_book if x.category.category is not None]
#         # small_categories = [x.category.category.category.name for x in selected_book \
#         #                     if x.category.category.category is not None]
#
#
#
# # """
# # SELECT ••• FROM "recommend_book" INNER JOIN "recommend_book_users" ON ("recommend_book"."id" = "recommend_book_users"."book_id") WHERE "recommend_book_users"."user_id" = '4'
# #  2 similar queries.  Duplicated 2 times.		0.14
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_book" INNER JOIN "recommend_book_users" ON ("recommend_book"."id" = "recommend_book_users"."book_id") INNER JOIN "recommend_smallcategory" ON ("recommend_book"."category_id" = "recommend_smallcategory"."id") LEFT OUTER JOIN "recommend_smallcategory" T5 ON ("recommend_smallcategory"."category_id" = T5."id") LEFT OUTER JOIN "recommend_smallcategory" T6 ON (T5."category_id" = T6."id") WHERE "recommend_book_users"."user_id" = '4'
# #  2 similar queries.  Duplicated 2 times.		0.23
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_book" INNER JOIN "recommend_book_users" ON ("recommend_book"."id" = "recommend_book_users"."book_id") WHERE "recommend_book_users"."user_id" = '4'
# #  2 similar queries.  Duplicated 2 times.		0.12
# # Sel Expl
# # +
# # SELECT ••• FROM "recommend_book" INNER JOIN "recommend_book_users" ON ("recommend_book"."id" = "recommend_book_users"."book_id") INNER JOIN "recommend_smallcategory" ON ("recommend_book"."category_id" = "recommend_smallcategory"."id") LEFT OUTER JOIN "recommend_smallcategory" T5 ON ("recommend_smallcategory"."category_id" = T5."id") LEFT OUTER JOIN "recommend_smallcategory" T6 ON (T5."category_id" = T6."id") WHERE "recommend_book_users"."user_id" = '4'
# #  2 similar queries.  Duplicated 2 times.
# # """
#
#
#         # ### 6 query, 1.19ms
#         selected_books = qs.filter(users=self.request.user)
#         selected_books_category = selected_books.select_related( "category",
#                                                                           "category__category",
#                                                                           "category__category__category", )
#         publishers = [x.publisher for x in selected_books]
#         authors = [x.author for x in selected_books]
#         large_categories = [x.category.name for x in selected_books_category]
#         medium_categories = [x.category.category.name for x in selected_books_category if x.category.category is not None]
#         small_categories = [x.category.category.category.name for x in selected_books_category \
#                             if x.category.category.category is not None]
#
#
# ########## 6 query, 1.08ms
#         # selected_books = qs.filter(users=self.request.user)
#         # selected_books_category = selected_books.select_related( "category",
#         #                                                                   "category__category",
#         #                                                                   "category__category__category", )
#         # publishers,authors = zip(*[(x['publisher'],x['author'])  for x in selected_books.values()])
#         # large_categories = [x.category.name for x in selected_books_category]
#         # medium_categories = [x.category.category.name for x in selected_books_category if x.category.category is not None]
#         # small_categories = [x.category.category.category.name for x in selected_books_category \
#         #                     if x.category.category.category is not None]
#
#
#
#         # 4 query, 0.93ms
#         # selected_book = qs.filter(users=self.request.user).values('author', 'publisher', 'category__name',\
#         #                                                           'category__category__name',\
#         #                                                             'category__category__category__name')
#         #
#         # publishers = [x['publisher'] for x in selected_book]
#         # authors = [x['author'] for x in selected_book]
#         # large_categories = [x['category__name'] for x in selected_book]
#         # medium_categories = [x['category__category__name'] for x in selected_book]
#         # small_categories = [x['category__category__category__name'] for x in selected_book]
#
#
#
#
# ######### 49 query 4.07ms
#         # results = []
#         # for q in qs:
#         #     preferred_weight = 0
#         #     if q.publisher in publishers:
#         #         preferred_weight += 0.5
#         #     if q.author in authors:
#         #         preferred_weight += 0.5
#         #     if q.category.name in large_categories:
#         #         preferred_weight += 0.4
#         #     if q.category.category:
#         #         if q.category.category.name in medium_categories:
#         #             preferred_weight += 0.3
#         #         if q.category.category.category:
#         #             if q.category.category.category.name in small_categories:
#         #                 preferred_weight += 0.2
#         #     preferred_weight += q.score * 0.1
#         #
#         #     results.append((q, preferred_weight))
#         #
#         # results = sorted(results, key=lambda x: x[1], reverse=True)
#         # results_id = [x.id for x, y in results][:3]
#         #
#         # #
#         # queryset = qs.filter(id__in=results_id)
#         # return queryset
#
# ######### 20 query 4.07ms
#         results = []
#         qs_b = qs.select_related( "category", "category__category","category__category__category", )
#
#         for q,b in zip(qs,qs_b):
#             preferred_weight = 0
#             if q.publisher in publishers:
#                 preferred_weight += 0.5
#             if q.author in authors:
#                 preferred_weight += 0.5
#             if b.category.name in large_categories:
#                 preferred_weight += 0.4
#             if b.category.category:
#                 if b.category.category.name in medium_categories:
#                     preferred_weight += 0.3
#                 if b.category.category.category:
#                     if b.category.category.category.name in small_categories:
#                         preferred_weight += 0.2
#             preferred_weight += q.score * 0.1
#
#             results.append((q, preferred_weight))
#
#         results = sorted(results, key=lambda x: x[1], reverse=True)
#         results_id = [x.id for x, y in results][:3]
#
#         # 10 query
#         queryset = qs.filter(id__in=results_id)
#         return queryset




#### 7 queries, 4.09ms
    def get_queryset(self):

        qs = super().get_queryset().select_related( "category","category__category", "category__category__category", ).all()

        selected_books = qs.filter(users=self.request.user)
        publishers = [x.publisher for x in selected_books]
        authors = [x.author for x in selected_books]
        large_categories = [x.category.name for x in selected_books]
        medium_categories = [x.category.category.name for x in selected_books if x.category.category is not None]
        small_categories = [x.category.category.category.name for x in selected_books \
                            if x.category.category.category is not None]


        results = []
        for q in qs:
            preferred_weight = 0
            if q.publisher in publishers:
                preferred_weight += 0.5
            if q.author in authors:
                preferred_weight += 0.5
            if q.category.name in large_categories:
                preferred_weight += 0.4
            if q.category.category:
                if q.category.category.name in medium_categories:
                    preferred_weight += 0.3
                if q.category.category.category:
                    if q.category.category.category.name in small_categories:
                        preferred_weight += 0.2
            preferred_weight += q.score * 0.1

            results.append((q, preferred_weight))

        results = sorted(results, key=lambda x: x[1], reverse=True)
        results_id = [x.id for x, y in results][:3]

        # 10 query
        queryset = qs.filter(id__in=results_id)
        return queryset













#
# class BookListFavoriteGenericAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]
#
#
#     # 선택한 책 중에 작가, 대,중,소 분류, 출판사가 있으면 가중치를 줌
#     # 그리고 가장 높은 가중치의 상위 3개만 띄워줌
#     def get_queryset(self):
#         qs = super().get_queryset()
#         # user_id = self.request.user.id
#         # contains : string
#         # list :
#         # selected_book = qs.filter(users__id__contains=user_id)
#         # 포함도 = users는 list / 단일
#         ## 왼쪽 single
#         ## 오른쪽 single
#
#         # 디비에 계속 접근 xxxx 한꺼번에 갖고 오기
#
#         # self -> 최하위만 갖고 -> 부모
#         # m2m
#
#
#         ### Returns a QuerySet that will “follow” foreign-key relationships,
#         # selecting additional related-object data when it executes its query.
#         # This is a performance booster which results in a single more complex query
#         # but means later use of foreign-key relationships won’t require database queries.
#         #### select_related 에서 author과 publisher는 에러
#         # If a non-related field is used like a relation,
#         # or if a single non-relational field is given.
#         ### FK 상황에서만 쓴다고 이해하면 되는건가
#         selected_book = qs.filter(users=self.request.user).select_related( "category",
#                                                                           "category__category",
#                                                                           "category__category__category", )
#
#
#         ### values
#         ## Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.
#
#
# ### If you have a field called foo that is a ForeignKey, the default values() call will return a dictionary key
#         # called foo_id, since this is the name of the hidden model attribute that stores the actual value
#         # (the foo attribute refers to the related model).
#         # When you are calling values() and passing in field names,
#         # you can pass in either foo or foo_id and you will get back the same thing
#         # (the dictionary key will match the field name you passed in).
#
#
#
#         selected_book = qs.filter(users=self.request.user).values('author', 'publisher', 'category__name',\
#                                                                   'category__category__name',\
#                                                                     'category__category__category__name')
#
#         publishers = [x['publisher'] for x in selected_book]
#         authors = [x['author'] for x in selected_book]
#         large_categories = [x['category__name'] for x in selected_book]
#         # medium_categories = [x['category__category__name'] for x in selected_book]
#         # small_categories = [x['category__category__category__name'] for x in selected_book]
#
#         results = []
#         for q in qs:
#             preferred_weight = 0
#             if q.publisher in publishers:
#                 preferred_weight += 0.5
#             if q.author in authors:
#                 preferred_weight += 0.5
#             if q.category.name in large_categories:
#                 preferred_weight += 0.4
#             # if q.category.category.name in medium_categories:
#             #     preferred_weight += 0.3
#             # if q.category.category.category.name in small_categories:
#             #     preferred_weight += 0.2
#             preferred_weight += q.score * 0.1
#
#             results.append((q, preferred_weight))
#
#         results = sorted(results, key=lambda x: x[1], reverse=True)
#         results_id = [x.id for x, y in results][:3]
#
#         #
#         queryset = qs.filter(id__in=results_id)
#         return queryset
