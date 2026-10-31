from django import forms

from book.models import Book
from .models import Order


class BookChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} (примірників: {obj.count})"


class OrderCreateForm(forms.Form):
    book = BookChoiceField(
        queryset=Book.objects.all().order_by("name"),
        label="Виберіть книгу",
        empty_label=None,
    )

    def clean_book(self):
        book = self.cleaned_data["book"]

        active_orders = Order.objects.filter(
            book=book,
            end_at__isnull=True,
        ).count()

        if active_orders >= book.count:
            raise forms.ValidationError("Немає доступних примірників цієї книги")

        return book


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["plated_end_at"]
        labels = {
            "plated_end_at": "Запланована дата повернення",
        }
        widgets = {
            "plated_end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def clean_plated_end_at(self):
        plated_end_at = self.cleaned_data["plated_end_at"]

        if self.instance.created_at and plated_end_at <= self.instance.created_at:
            raise forms.ValidationError(
                "Дата повернення має бути пізнішою за дату замовлення"
            )

        return plated_end_at
