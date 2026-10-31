from django import forms

from author.models import Author
from .models import Book


class AuthorMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"


class BookForm(forms.ModelForm):
    authors = AuthorMultipleChoiceField(
        queryset=Author.objects.all().order_by("surname", "name"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Автори",
    )

    class Meta:
        model = Book
        fields = ["name", "description", "count", "authors"]
        labels = {
            "name": "Назва",
            "description": "Опис",
            "count": "Кількість примірників",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].required = True
        self.fields["count"].min_value = 0
        self.fields["count"].widget.attrs["min"] = 0

        if self.instance.pk:
            self.fields["authors"].initial = self.instance.authors.all()

    def clean_count(self):
        count = self.cleaned_data["count"]

        if count < 0:
            raise forms.ValidationError("Кількість не може бути від'ємною")

        return count

    def save(self, commit=True):
        book = super().save(commit=commit)

        if commit:
            book.authors.set(self.cleaned_data["authors"])
        else:
            original_save_m2m = self.save_m2m

            def save_m2m():
                original_save_m2m()
                book.authors.set(self.cleaned_data["authors"])

            self.save_m2m = save_m2m

        return book
