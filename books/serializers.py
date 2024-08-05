from rest_framework import serializers
from .models import Book, Recommendation, User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Recommendation
        fields = ['id', 'book', 'user', 'comments', 'likes', 'created_at', 'updated_at']
