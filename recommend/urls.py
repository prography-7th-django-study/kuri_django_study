from django.urls import path, include
from rest_framework import routers

from .views import BookListGenericAPIView, BookListFavoriteGenericAPIView, BookListSelectGenericAPIView, BookCRUD, CategoryCRUD




router = routers.DefaultRouter()
router.register(r'books/upload', BookCRUD)
router.register(r'category/upload', CategoryCRUD)

urlpatterns = [

    path('books', BookListGenericAPIView.as_view(), name='books'),
    # path('users/{user_id}/books/favorite', BookListFavoriteGenericAPIView.as_view(), name='favorite_book')
    path('books/recommend', BookListFavoriteGenericAPIView.as_view(), name='recommend_book'),
    path('books/select', BookListSelectGenericAPIView.as_view(), name='selected_book'),
    path('', include(router.urls)),

]
