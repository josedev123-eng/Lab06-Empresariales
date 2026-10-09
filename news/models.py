from django.db import models


class Category(models.Model):
    """Categoría de noticias (tabla news_category, sin choque con library)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'categoría (noticias)'
        verbose_name_plural = 'categorías (noticias)'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'autor (noticias)'
        verbose_name_plural = 'autores (noticias)'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    published_at = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'noticia'
        verbose_name_plural = 'noticias'

    def __str__(self):
        return self.title
