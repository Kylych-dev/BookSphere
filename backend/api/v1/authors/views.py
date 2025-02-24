from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.library.models import Author, FavoriteBook
from api.v1.books.serializers import AuthorSerializer, FavoriteBookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'detail': f'Автор {instance.first_name} {instance.last_name} удалён.'},
                status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {'detail': 'Автор уже удалён или не существует.'},
                status=status.HTTP_404_NOT_FOUND)

class FavoriteBookViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteBookSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)

    @action(detail=True, methods=['delete'])
    def clear(self, request):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {'detail': 'У вас нет избранных книг.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'detail': 'Все избранные книги удалены.'},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)