from django.contrib import admin
from django.utils.html import format_html

from .models import Article, Author, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count']
    search_fields = ['name']

    @admin.display(description='Noticias')
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'name', 'email']
    search_fields = ['name', 'email']

    @admin.display(description='Foto')
    def thumb(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:36px;height:36px;object-fit:cover;border-radius:50%">', obj.avatar.url)
        return '—'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'author', 'display_categories', 'published_at']
    list_filter = ['categories', 'published_at', 'author']
    search_fields = ['title', 'body', 'author__name']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_at'
    filter_horizontal = ['categories']

    @admin.display(description='Imagen')
    def thumb(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="width:64px;height:40px;object-fit:cover;border-radius:6px">', obj.featured_image.url)
        return '—'

    @admin.display(description='Categorías')
    def display_categories(self, obj):
        return ', '.join(c.name for c in obj.categories.all())
