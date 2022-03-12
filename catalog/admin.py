from django.contrib import admin

from .models import Author, Book, Language, Publisher, Tag


admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Tag)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'display_author',
        'publisher',
        'year',
        'isbn'
    )
    list_filter = (
        'publisher',
        'year'
    )
    ordering = (
        'title',
    )

    def display_author(self, object):
        authors = ', '.join(
            '{} {}'.format(author.first_name, author.last_name)
            for author in object.author.all()
        )
        return authors
    
    display_author.short_description = 'Author'
