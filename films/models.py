from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import datetime


class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Genre(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Person(MyModel):
    name = models.CharField("Имя", max_length=400)
    origin_name = models.CharField("Имя в оригинале", max_length=400,
                                   blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True,
                                validators=[
                                    MaxValueValidator(
                                        limit_value=datetime.date.today)
                                ])
    photo = models.ImageField(
        "Фото", upload_to='photos/', blank=True, null=True)
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    def age(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        return today.year - self.birthday.year \
            - ((today.month, today.day) < (self.birthday.month,
                                           self.birthday.day))

    class Meta:
        ordering = ["name"]
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self):
        return self.name


class Film(MyModel):
    name = models.CharField("Имя", max_length=1024)
    origin_name = models.CharField(
        "Название (в оригинале)", max_length=1024, blank=True, null=True)
    slogan = models.CharField("Девиз", max_length=2048, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Страна")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    director = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="Режиссер",
        related_name="directed_films")
    length = models.PositiveIntegerField(
        "Продолжительность", blank=True, null=True)
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True,
                                       validators=[MinValueValidator(
                                           limit_value=1885)])
    trailer_url = models.URLField("Трейлер", blank=True, null=True)
    cover = models.ImageField(
        "Постер", upload_to='covers/', blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    people = models.ManyToManyField(Person, verbose_name="Актеры") # film_set в качестве related_name ??? views.py 195
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name


class Book(MyModel):
    name = models.CharField("Название книги", max_length=200)
    author = models.CharField("Автор книги", max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    published_at = models.DateTimeField() # Валидатор поставить!
    description = models.TextField("Описание книги", blank=True)
    length = models.PositiveIntegerField("Количество страниц", blank=True, null=True)
    booksCover = models.ImageField(
        "Обложка книги", upload_to='booksCover/', blank=True, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    publisher = models.CharField("Издательство", max_length=200)
    ISBN = models.CharField("Международный номер", max_length = 15, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.name


class Cart(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through="CartItem")
    is_active = models.BooleanField("Активность корзины")

    class Meta:
        ordering = ["user"]
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(MyModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    historic_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ["cart"]
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.count} x {self.book.name}"
