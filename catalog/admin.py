from django.contrib import admin, messages
from django.db.models import F

import datetime

from .models import *

# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']
    ordering = ['first_name', 'last_name']
    list_filter = ['last_name']
    search_fields = ['last_name']
    inlines = [BookInline]
    readonly_fields = ['last_name']
    # fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
    fieldsets = (
        ('Name', {
            'fields': ('first_name', 'last_name')
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('date_of_birth', 'date_of_death')
        })
    )
    actions = ['died']

    def died(self, request, queryset):
        # updated = queryset.update(pages_count=F('pages_count') + 2)
        updated = queryset.update(date_of_death=datetime.date.today())
        self.message_user(
            # request, f"{updated} books pages added with two", messages.SUCCESS
            request, f"{updated} died!", messages.SUCCESS
        )

    died.short_description = 'Die selected authors'


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'language', 'display_genre']
    list_filter = ['genre', 'language']
    search_fields = ['title']
    inlines = [BookInstanceInline]
    readonly_fields = ['title']
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'author')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': (('summary', 'isbn'), ('genre', 'language'))
        })
    )
    actions = ['change_language_to_persian', 'change_language_to_english']

    def change_language_to_persian(self, request, queryset):
        updated = queryset.update(language=Language.objects.get(name='Persian'))
        self.message_user(
            request, f"{updated} Book's language change to Persian", messages.SUCCESS
        )
    change_language_to_persian.short_description = 'Change Language to Persian'

    def change_language_to_english(self, request, queryset):
        updated = queryset.update(language=Language.objects.get(name='English'))
        self.message_user(
            request, f"{updated} Book's language change to English", messages.SUCCESS
        )
    change_language_to_english.short_description = 'Change Language to English'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')
    search_fields = ('book',)
    actions = ['change_status_to_available']
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

    def change_status_to_available(self, request, queryset):
        updated = queryset.update(
            status=BookInstance.LoanStatus.AVAILABLE,
            due_back=None,
            borrower=None
        )
        self.message_user(
            request, f"{updated} Book Instances status change to Available", messages.SUCCESS
        )
    change_status_to_available.short_description = 'Change status to Available'
