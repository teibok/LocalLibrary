from django.contrib import admin

# Register your models here.
from .models import Author,Genre,Book,BookInstance

"""admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)
admin.site.register(Genre)
"""

"""class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name','first_name','date_of_birth','date_of_death')
    fields=['first_name','last_name','date_of_birth','date_of_death']"""

admin.site.register(Author)
#admin.site.register(Author, AuthorAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter=('status','due_back')
    fieldsets = (
        ('Happy', {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower',)
        }),
    )
