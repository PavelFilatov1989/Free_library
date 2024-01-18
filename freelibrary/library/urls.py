from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.LibraryHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addbook/', views.AddBook.as_view(), name='add_book'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('book/<slug:book_slug>/', views.show_book, name='book'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_booklist, name='tag'),

]