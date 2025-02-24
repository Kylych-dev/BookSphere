from rest_framework import serializers
from apps.library.models import (
    Book,
    Author,
    Genre,
    FavoriteBook
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # authors = AuthorSerializer(many=True, read_only=True)
    authors = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, read_only=True)

    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all(),
        source='book_authors',
        write_only=True
    )

    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source='genres',
        write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'summary',
            'isbn',
            'authors',
            'genres',
            'author_ids',
            'genre_ids',
            'publication_date'
        ]
        extra_kwargs = {
            'isbn': {'validators': []},
        }

    def get_authors(self, obj):
        return [
            {"id": ba.author.id, "name": f"{ba.author.first_name} {ba.author.last_name}"}
            for ba in obj.book_authors.all()
        ]


class FavoriteBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = FavoriteBook
        fields = ['id', 'book_title', 'created_at']
        read_only_fields = ['user', 'created_at']

    # def create(self, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     return super().create(validated_data)