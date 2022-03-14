from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .models import Author, Book


def index(request):
    """Представление для главной страницы"""
    book_list = Book.objects.all()[:6]
    author_list = Author.objects.order_by('last_name').all()
    context = {
        'book_list': book_list,
        'author_list': author_list
    }
    return render(request, 'index.html', context=context)


def search(request):
    """Представление для поиска"""
    query = request.GET.get('q')
    book_list = Book.objects.filter(
        Q(title__icontains=query) | Q(summary__icontains=query)
    )
    author_list = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    context = {
        'book_list': book_list,
        'author_list': author_list
    }
    return render(request, 'search.html', context=context)


class BookListView(generic.ListView):
    """Представление списка книг"""
    paginate_by = 18
    model = Book


class BookDetailView(generic.DetailView):
    """Детальной представление книги"""
    model = Book


class AuthorListView(generic.ListView):
    """Представление списка авторов"""
    model = Author

    def get_queryset(self):
        """Возвращает кверисет, отсортированный по фамилии"""
        queryset = Author.objects.order_by('last_name').all()
        return queryset


class AuthorDetailView(generic.DetailView):
    """Детальное представление автора"""
    model = Author
