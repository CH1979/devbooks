from django.db.models import Count
from django.views import generic

from .models import Author, Book


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author

    def get_queryset(self):
        """Дополняет кверисет количеством книг, написанных автором"""
        queryset = Author.objects.all().annotate(book_count = Count('book'))
        return queryset


class AuthorDetailView(generic.DetailView):
    model = Author
