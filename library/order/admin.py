from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'created_at', 'plated_end_at', 'end_at', 'is_returned')
    list_display_links = ('id',)
    list_filter = ('created_at', 'plated_end_at', 'end_at')
    search_fields = ('id', 'book__name', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Книга і читач', {'fields': ('book', 'user')}),
        ('Дати', {'fields': ('created_at', 'plated_end_at', 'end_at')}),
    )

    @admin.display(boolean=True, description='Повернена')
    def is_returned(self, obj):
        return obj.end_at is not None
