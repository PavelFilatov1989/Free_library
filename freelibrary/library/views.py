from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import AddBookForm
from .models import Library, Category, TagPost

menu = [{'title': "о библиотеке", 'url_name': 'about'},
        {'title': "добавить книгу", 'url_name': 'add_book'},
        {'title': "искать книгу", 'url_name': 'search'},
        {'title': "обратная связь", 'url_name': 'contact'},
        {'title': "войти/Регистрация", 'url_name': 'login'}
]


def index(request):
    books = Library.published.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'books': books,
        'cat_selected': 0,
    }
    return render(request, 'library/index.html', context=data)

def about(request):
    data = {
        'title': 'О библиотеке',
        'menu': menu,
    }
    return render(request, 'library/about.html', context=data)

def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddBookForm()
    data = {
        'title': 'Добавление книги',
        'menu': menu,
        'form': form,
    }
    return render(request, 'library/add_book.html', context=data)

def search(request):
    return HttpResponse("Искать книгу")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Войти/Регистрация")

def show_book(request, book_slug):
    book = get_object_or_404(Library, slug=book_slug)
    data = {
        'title': book.author,
        'menu': menu,
        'book': book,
        'cat_selected': 1,
    }
    return render(request, 'library/book.html', context=data)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    books = Library.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Жанр: {category.name}',
        'menu': menu,
        'books': books,
        'cat_selected': category.pk,
    }
    return render(request, 'library/index.html', context=data)


def show_tag_booklist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    books = tag.tags.filter(is_published=Library.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'books': books,
        'cat_selected': None,
    }
    return render(request, 'library/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена </h1")