from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from .forms import AddBookForm, UploadFileForm
from .models import Library, Category, TagPost, UploadFiles
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .utils import DataMixin


class LibraryHome(DataMixin, ListView):
    template_name = 'library/index.html'
    context_object_name = 'books'
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        return Library.published.all().select_related('cat')


@login_required
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

        'form': form
    }
    return render(request, 'library/about.html', context=data)


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'library/add_book.html'
    title_page = 'Добавление книги'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author_add = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Library
    fields = '__all__'
    template_name = 'library/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование книги'


def search(request):
    return HttpResponse("Искать книгу")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Войти/Регистрация")

class ShowBook(DataMixin, DetailView):
    template_name = 'library/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['book'])

    def get_object(self, queryset=None):
        return get_object_or_404(Library.published, slug=self.kwargs[self.slug_url_kwarg])



class LibraryCategory(DataMixin, ListView):
    template_name = 'library/index.html'
    context_object_name = 'books'
    allow_empty = False


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['books'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )

    def get_queryset(self):
        return Library.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')



class TagBookList(DataMixin, ListView):
    template_name = 'library/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


    def get_queryset(self):
        return Library.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена </h1")