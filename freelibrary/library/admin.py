from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Library, Category


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    fields = ['author', 'book', 'content', 'photo', 'post_photo', 'cat', 'tags']
    readonly_fields = ['post_photo']
    #prepopulated_fields = {'slug': ('book', )}
    filter_horizontal = ['tags']
    list_display = ('author', 'book', 'content', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('author', 'book')
    ordering = ['time_create', 'author']
    list_editable = ('is_published',)
    list_per_page = 6
    actions = ['set_published', 'set_draft']
    search_fields = ['author', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True

    @admin.display(description='Изображение')
    def post_photo(self, book: Library):
        if book.photo:
            return mark_safe(f"<img src='{book.photo.url}' width=50>")
        return "Без фото"

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
