from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404
from .serializers import *


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=False, methods=['post'])
    def signup(self, request):
        try:
            serializer = UserSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save(is_active=True)
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({"success": True, 'message': 'User Register Successfully.'},
                                status=status.HTTP_201_CREATED)
            return Response({"success": False, 'message': serializer.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        try:
            data = request.data.copy()
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(request, email=email, password=password)

            if not user:
                raise AuthenticationFailed('Invalid Credentials.')

            if user is not None:
                return Response({
                    'access': user.tokens()['access'],
                    'refresh': user.tokens()['refresh'],
                }, status=status.HTTP_200_OK)

            return Response({'success': False, 'message': "Invalid Credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"success": False, 'error': err.args[0]})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['post'])
    def fetch_and_save_books(self, request):
        query = "harry+potter"
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            books_data = response.json().get('items', [])
            for book_data in books_data:
                volume_info = book_data.get('volumeInfo', {})

                title = volume_info.get('title', '')
                authors = volume_info.get('authors', [])
                author = ', '.join(authors) if authors else 'Unknown'
                description = volume_info.get('description', '')
                cover_image = volume_info.get('imageLinks', {}).get('thumbnail', '')
                ratings = volume_info.get('averageRating', 0.0)

                book = Book(
                    title=title,
                    author=author,
                    description=description,
                    cover_image=cover_image,
                    ratings=ratings
                )
                book.save()

            return Response({'success': True, 'message': 'Books data saved successfully!'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to fetch data from Google Books API'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def book_list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True).data
        return Response({'success': True, 'data': serializer}, status=status.HTTP_200_OK)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def comment(self, request):
        data = request.data.copy()
        book_id = data.get('book_id', None)
        comment = data.get('comment', None)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Http404(f"Book not found in the database.")
        model_obj = Recommendation(book=book, comments=comment, user=self.request.user)
        model_obj.save()
        return Response({'success': True, 'message': "Comment on the Books."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        try:
            recommendation = self.get_object()
            recommendation.likes.add(request.user)
            recommendation.save()
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)
        except Recommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def book_recommendations(self, request):
        book_id = request.query_params.get('book_id')
        if book_id:
            recommendations = self.queryset.filter(book_id=book_id)
            serializer = self.get_serializer(recommendations, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'book_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
