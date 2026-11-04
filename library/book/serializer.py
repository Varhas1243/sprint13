from rest_framework import serializers

from author.models import Author
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all(),
        required=False,
    )

    class Meta:
        model = Book
        fields = ["id", "name", "description", "count", "authors"]

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop("authors", None)
        book = super().update(instance, validated_data)

        if authors is not None:
            book.authors.set(authors)

        return book
