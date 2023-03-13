from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html

from library.actions import change_status_selected, cancel_book_selected, set_null_quantity
from library.models import Book, Author
from urllib.parse import quote as urlquote

User = get_user_model()

admin.site.register(Author)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', '_author', 'quantity')
    search_fields = ('title',)
    actions = (set_null_quantity,)

    def _author(self, obj: Book):
        opts = obj._meta
        redirect_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, 'author'),
            args=(quote(obj.author.pk),),
            current_app=self.admin_site.name,)
        return format_html('<a href="{}">{}</a>', urlquote(redirect_url), obj.author)

    _author.short_description = 'Автор'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'is_active', 'display_book')
    list_filter = ('is_active',)
    list_display_links = ('first_name', 'last_name', 'username')
    actions = [change_status_selected, cancel_book_selected]
    search_fields = ('first_name', 'last_name', 'username')
