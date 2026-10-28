from django.contrib import admin

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'patronymic', 'books_count')
    list_display_links = ('id', 'surname')
    list_filter = ('id', 'surname', 'name')
    search_fields = ('id', 'name', 'surname', 'patronymic', 'books__name')
    ordering = ('id',)
    fieldsets = (
        ('Особисті дані автора', {
            'fields': ('name', 'surname', 'patronymic'),
        }),
        ('Книги автора', {
            'fields': ('books',),
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        formfield = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'books':
            formfield.required = False
        return formfield

    @admin.display(description='Кількість книг')
    def books_count(self, obj):
        return obj.books.count()