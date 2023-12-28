from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Library.Status.PUBLISHED)

class Library(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    author = models.CharField(max_length=255, verbose_name = 'Автор')
    book = models.CharField(max_length=255, verbose_name = 'Книга')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            validators=[
                                MinLengthValidator(5, message="Минимум 5 символов"),
                                MaxLengthValidator(100, message="Максимум 100 символов"),
                            ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",
                              default=None,
                              blank=True,
                              null=True,
                              verbose_name="Фото")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name = 'Состояние')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='cats', verbose_name = 'Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
