from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from .models import Author, Book


def index(request):
    book_list = Book.objects.all()[:6]
    author_list = Author.objects.order_by('last_name').all()
    context = {
        'book_list': book_list,
        'author_list': author_list
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    paginate_by = 18
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author

    def get_queryset(self):
        """Возвращает кверисет, отсортированный по фамилии"""
        queryset = Author.objects.order_by('last_name').all()
        return queryset


class AuthorDetailView(generic.DetailView):
    model = Author
