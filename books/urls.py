from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user_registrations'),
router.register(r'book', views.BookViewSet, basename='books-create-fetch'),
router.register(r'recommend', views.RecommendationViewSet, basename='recommend-books'),

urlpatterns = [
    path('', include(router.urls)),
]
