from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Article, Category


def home(request):
    """Portada: últimas noticias ya publicadas."""
    articles = (
        Article.objects.filter(published_at__lte=timezone.now())
        .select_related('author')
        .prefetch_related('categories')
    )
    categories = Category.objects.all()
    return render(request, 'news/home.html', {'articles': articles, 'categories': categories})


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug,
    )
    related = (
        Article.objects.filter(categories__in=article.categories.all())
        .exclude(pk=article.pk)
        .distinct()
        .select_related('author')[:3]
    )
    return render(request, 'news/article_detail.html',
                    {'article': article, 'related': related, 'categories': Category.objects.all()})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = (
        category.articles.filter(published_at__lte=timezone.now())
        .select_related('author')
        .prefetch_related('categories')
    )
    categories = Category.objects.all()
    return render(
        request, 'news/category_list.html',
        {'category': category, 'articles': articles, 'categories': categories},
    )
