from django.contrib import admin, messages
from .models import Library, Category


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('author', 'book', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('author', 'book')
    ordering = ['time_create', 'author']
    list_editable = ('is_published',)
    list_per_page = 6
    actions = ['set_published', 'set_draft']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, book: Library):
        return f"Описание {len(book.content)} символов"

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Library.Status.PUBLISHED)
        self.message_user(request, f'изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Library.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


#admin.site.register(Library, LibraryAdmin)
