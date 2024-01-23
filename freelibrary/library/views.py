from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from .forms import AddBookForm, UploadFileForm
from .models import Library, Category, TagPost, UploadFiles
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

menu = [{'title': "о библиотеке", 'url_name': 'about'},
        {'title': "добавить книгу", 'url_name': 'add_book'},
        {'title': "искать книгу", 'url_name': 'search'},
        {'title': "обратная связь", 'url_name': 'contact'},
        {'title': "войти/Регистрация", 'url_name': 'login'}
]


# def index(request):
#     books = Library.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'books': books,
#         'cat_selected': 0,
#     }
#     return render(request, 'library/index.html', context=data)


class LibraryHome(ListView):
    model = Library
    template_name = 'library/index.html'
    context_object_name = 'books'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Library.published.all().select_related('cat')

    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'books': Library.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {
        'title': 'О библиотеке',
        'menu': menu,
        'form': form
    }
    return render(request, 'library/about.html', context=data)

# def add_book(request):
#     if request.method == 'POST':
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddBookForm()
#     data = {
#         'title': 'Добавление книги',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'library/add_book.html', context=data)

class AddBook(CreateView):
    form_class = AddBookForm
    template_name = 'library/add_book.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление книги',
    }

class UpdatePage(UpdateView):
    model = Library
    fields = '__all__'
    template_name = 'library/add_book.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование книги',
    }


# class AddBook(View):
#     def get(self, request):
#         form = AddBookForm()
#         data = {
#             'title': 'Добавление книги',
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'library/add_book.html', context=data)
#
#     def post(self, request):
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'title': 'Добавление книги',
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'library/add_book.html', context=data)


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

class ShowBook(DetailView):
    #model = Library
    template_name = 'library/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['book']
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Library.published, slug=self.kwargs[self.slug_url_kwarg])


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     books = Library.published.filter(cat_id=category.pk).select_related('cat')
#     data = {
#         'title': f'Жанр: {category.name}',
#         'menu': menu,
#         'books': books,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'library/index.html', context=data)


class LibraryCategory(ListView):
    template_name = 'library/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['books'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Library.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


# def show_tag_booklist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     books = tag.tags.filter(is_published=Library.Status.PUBLISHED).select_related('cat')
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'books': books,
#         'cat_selected': None,
#     }
#     return render(request, 'library/index.html', context=data)


class TagBookList(ListView):
    template_name = 'library/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Library.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена </h1")