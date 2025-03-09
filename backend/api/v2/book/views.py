from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.library.models import Book


class BookList(APIView):
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)