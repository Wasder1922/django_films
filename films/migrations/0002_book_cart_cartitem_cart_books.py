# Generated by Django 5.1.4 on 2024-12-23 19:46

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='Название книги')),
                ('author', models.CharField(max_length=200, verbose_name='Автор книги')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('published_at', models.DateTimeField()),
                ('description', models.TextField(blank=True, verbose_name='Описание книги')),
                ('length', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество страниц')),
                ('booksCover', models.ImageField(blank=True, null=True, upload_to='booksCover/', verbose_name='Обложка книги')),
                ('publisher', models.CharField(max_length=200, verbose_name='Издательство')),
                ('ISBN', models.CharField(max_length=15, verbose_name='Международный номер')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.film')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(verbose_name='Активность корзины')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('historic_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.cart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='books',
            field=models.ManyToManyField(through='films.CartItem', to='films.book'),
        ),
    ]
