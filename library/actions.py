from django.contrib import admin

from library.models import Book


@admin.action(description='Изменить статус')
def change_status_selected(self, request, queryset):
    for reader in queryset.all():
        reader.is_active = False if reader.is_active else True
        reader.save()


@admin.action(description='Удалить книги из актива читателя')
def cancel_book_selected(self, request, queryset):

    for reader in queryset.all():
        for book in reader.book.all():
            book = Book.objects.get(pk=book.pk)
            book.quantity += 1
            book.save()
            reader.book.remove(book)


@admin.action(description='Установить кол-во 0')
def set_null_quantity(self, request, queryset):
    queryset.update(quantity=0)
