from rest_framework import serializers
from apps.library.models import (
    Book,
    BookAuthor,
    FavoriteBook,
    Author,
    Genre
)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'summary']

