from django.contrib import admin
from .models import Country, Film, Person, Genre, Book, Cart, CartItem

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartItem)
