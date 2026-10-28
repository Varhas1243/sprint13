from django.contrib import admin

from author.models import Author
from order.models import Order
from .models import Book


class AuthorFilter(admin.SimpleListFilter):

    title = 'автор'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        return [(a.pk, f'{a.surname} {a.name}') for a in Author.objects.order_by('surname', 'name')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(authors__pk=self.value())
        return queryset


class OrderInline(admin.TabularInline):

    model = Order
    extra = 0
    can_delete = False
    fields = ('user', 'created_at', 'plated_end_at', 'end_at')
    readonly_fields = ('created_at',)
    verbose_name = 'Видача книги'
    verbose_name_plural = 'Видачі книги (дата видачі, планова дата та дата повернення)'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'authors_list', 'description', 'count', 'last_issue_date')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name', AuthorFilter)
    search_fields = ('id', 'name', 'authors__name', 'authors__surname')
    ordering = ('id',)
    inlines = [OrderInline]
    fieldsets = (
        ('Незмінні дані', {
            'fields': ('name', 'authors_list', 'description'),
        }),
        ('Змінні дані', {
            'fields': ('count',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):

        if obj:
            return ('name', 'authors_list', 'description')
        return ('authors_list',)

    @admin.display(description='Автори')
    def authors_list(self, obj):
        if not obj or not obj.pk:
            return 'Авторів можна додати на сторінці автора'
        return ', '.join(f'{a.surname} {a.name}' for a in obj.authors.all()) or '—'

    @admin.display(description='Остання видача')
    def last_issue_date(self, obj):
        order = Order.objects.filter(book=obj).order_by('-created_at').first()
        return order.created_at if order else '—'
