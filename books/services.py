import requests


class GoogleBooksService:
    @staticmethod
    def search_books():
        url = "https://www.googleapis.com/books/v1/volumes?q=harry+potter"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        books = [
            {
                'title': item['volumeInfo'].get('title', 'N/A'),
                'authors': item['volumeInfo'].get('authors', []),
                'description': item['volumeInfo'].get('description', 'N/A'),
                'cover_image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'N/A'),
                'ratings': item['volumeInfo'].get('averageRating', 'N/A')
            }
            for item in data.get('items', [])
        ]
        return books
