menu = [{'title': "о библиотеке", 'url_name': 'about'},
        {'title': "добавить книгу", 'url_name': 'add_book'},
        {'title': "искать книгу", 'url_name': 'search'},
        {'title': "обратная связь", 'url_name': 'contact'},

]


class DataMixin:
    paginate_by = 3
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected


    def get_mixin_context(self, context, **kwargs):

        context['cat_selected'] = None
        context.update(kwargs)
        return context