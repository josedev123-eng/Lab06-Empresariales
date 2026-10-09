"""Seed del portal news: 3 categorías, 2 autores, 6 noticias.
Una noticia incluye una etiqueta HTML en el cuerpo para la prueba de escapado (paso 12).
"""
import os
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pathlib import Path  # noqa: E402

from django.utils import timezone  # noqa: E402
from django.utils.text import slugify  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from news.models import Article, Author, Category  # noqa: E402

BASE = Path(__file__).resolve().parent
IMGDIR = BASE / 'media' / 'articles'
IMGDIR.mkdir(parents=True, exist_ok=True)


def font(size):
    for name in ('arial.ttf', 'DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_image(fname, title, top, bottom):
    img = Image.new('RGB', (800, 450), top)
    d = ImageDraw.Draw(img)
    for y in range(450):
        t = y / 449
        d.line([(0, y), (800, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    f = font(52)
    words, lines, cur = title.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= 700:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    y = 225 - len(lines) * 32
    for line in lines[:3]:
        d.text(((800 - d.textlength(line, font=f)) / 2, y), line, font=f, fill='white')
        y += 64
    path = IMGDIR / fname
    img.save(path, 'JPEG', quality=85)
    return f'articles/{fname}'


cats = {}
for name, desc in [
    ('Tecnología', 'Software, IA y gadgets.'),
    ('Deportes', 'Resultados y crónicas.'),
    ('Cultura', 'Cine, libros y arte.'),
]:
    c, _ = Category.objects.get_or_create(slug=slugify(name), defaults={'name': name, 'description': desc})
    cats[name] = c

authors = {}
for name, email in [('Lucía Ramos', 'lucia@example.com'), ('Marco Díaz', 'marco@example.com')]:
    a, _ = Author.objects.get_or_create(email=email, defaults={'name': name})
    authors[name] = a

now = timezone.now()
data = [
    ('La IA llega a las aulas', 'Tecnología', 'Lucía Ramos', 1, (15, 23, 42), (37, 99, 235),
     'Cómo los colegios usan la inteligencia artificial.',
     'La inteligencia artificial ya está en las aulas.\nLos docentes la usan para preparar clases.'),
    ('Nuevo récord de velocidad en chips', 'Tecnología', 'Marco Díaz', 2, (30, 10, 60), (120, 40, 180),
     'Un laboratorio anuncia un chip un 40% más rápido.',
     'El anuncio sorprendió al sector.\nLos expertos piden cautela ante las cifras.'),
    ('Final soñada en el campeonato', 'Deportes', 'Marco Díaz', 3, (0, 60, 20), (20, 160, 60),
     'Crónica de una final inolvidable.',
     'El partido se definió en el último minuto.\nLa afición celebró hasta altas horas.'),
    ('El club ficha a una joven promesa', 'Deportes', 'Lucía Ramos', 4, (80, 20, 0), (220, 120, 20),
     'El fichaje más esperado del verano.',
     'La delantera firmó por tres temporadas.\n<b>Etiqueta de prueba:</b> este texto muestra el escapado automático.'),
    ('Festival de cine anuncia su cartel', 'Cultura', 'Lucía Ramos', 5, (60, 0, 40), (180, 40, 120),
     'Diez días de estrenos y retrospectivas.',
     'El festival abrirá con una gala especial.\nHabrá entradas populares para estudiantes.'),
    ('La biblioteca reabre sus puertas', 'Cultura', 'Marco Díaz', 6, (0, 40, 80), (30, 140, 200),
     'Tras meses de obras, vuelve la sala central.',
     'La colección crece con mil títulos nuevos.\nEl horario se amplía los fines de semana.'),
]

for i, (title, cat, auth, days, top, bottom, excerpt, body) in enumerate(data):
    slug = slugify(title)
    art, created = Article.objects.get_or_create(
        slug=slug,
        defaults={'title': title, 'excerpt': excerpt, 'body': body,
                  'published_at': now - timedelta(days=days), 'author': authors[auth]},
    )
    if created:
        art.featured_image.name = make_image(f'{slug}.jpg', title, top, bottom)
        art.save(update_fields=['featured_image'])
    art.categories.set([cats[cat]])

print('Seed news OK')
print(f'Categorías: {Category.objects.count()} | Autores: {Author.objects.count()} | Noticias: {Article.objects.count()}')
