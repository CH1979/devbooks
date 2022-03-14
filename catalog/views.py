from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, Tag


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


class BookListView(generic.TemplateView):
    """Представление списка книг"""
    template_name = 'catalog/book_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        year = self.request.GET.get('year')
        tag = self.request.GET.get('tag')
        page_number = self.request.GET.get('page')

        queryset = Book.objects.all()
        if year is not None:
            try:
                year = int(year)
                queryset = queryset.filter(year__exact=year)
            except ValueError:
                raise Http404
        if tag is not None:
            try:
                tag = int(tag)
                queryset = queryset.filter(tag__exact=tag)
            except ValueError:
                raise Http404
        context['book_list'] = queryset

        paginator = Paginator(queryset, 18)
        context['book_list'] = paginator.get_page(page_number)

        year_list = Book.objects.values_list('year', flat=True)
        context['year_list'] = sorted(
            [x for x in set(year_list) if x is not None]
        )

        tag_list = Tag.objects.all()
        context['tag_list'] = tag_list
        return context


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
