from django import forms

from book.models import Book
from .models import Author


class BookMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AuthorForm(forms.ModelForm):
    books = BookMultipleChoiceField(
        queryset=Book.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Книги",
    )

    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic", "books"]
        labels = {
            "name": "Ім'я",
            "surname": "Прізвище",
            "patronymic": "По батькові",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ("name", "surname", "patronymic"):
            self.fields[field_name].required = True
