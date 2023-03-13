from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import User, Book


class UserSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='title', many=True)
    password = serializers.CharField(write_only=True, allow_blank=True)
    password_repeat = serializers.CharField(write_only=True, allow_blank=True)

    def validate(self, attrs):
        if attrs.get('password'):
            password = attrs['password']
            password_repeat = attrs.pop('password_repeat')

            if password != password_repeat:
                raise serializers.ValidationError('Passwords don\'t match')

        if attrs.get('book'):
            if len(attrs['book']) > 3:
                raise serializers.ValidationError('Can\'t add more than 3 books')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('book'):
            # Уменьшаем количество экземпляров книги, если книга добавляется в актив читателя
            for book in validated_data['book']:
                if book not in instance.book.all():
                    if book.quantity > 0:
                        book.quantity -= 1
                        book.save()
                    else:
                        raise ValidationError(f'The book {book.title} is missing')
            # Увеличиваем количество экземпляров книги, если книга удаляется из актива читателя
            for book in instance.book.all():
                if book not in validated_data['book']:
                    book.quantity += 1
                    book.save()

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'password_repeat', 'book']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'password_repeat']

    def validate(self, attrs):
        password = attrs['password']
        password_repeat = attrs.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Passwords don\'t match')

        return attrs
