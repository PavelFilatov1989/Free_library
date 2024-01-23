from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.LibraryHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addbook/', views.AddBook.as_view(), name='add_book'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('book/<slug:book_slug>/', views.ShowBook.as_view(), name='book'),
    path('category/<slug:cat_slug>/', views.LibraryCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagBookList.as_view(), name='tag'),

]