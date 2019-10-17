# Generated by Django 2.2.6 on 2019-10-17 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'categorytype',
                'verbose_name_plural': 'categorytypes',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bangazonapp.Customer')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('location', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='.static/media')),
                ('category_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='bangazonapp.CategoryType')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='bangazonapp.Customer')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='recommendations', to='bangazonapp.Product')),
                ('receive_customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receive_recommendations', to='bangazonapp.Customer')),
                ('send_customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='send_recommendations', to='bangazonapp.Customer')),
            ],
            options={
                'verbose_name': 'recommendation',
                'verbose_name_plural': 'recommendations',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ratings', to='bangazonapp.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ratings', to='bangazonapp.Product')),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('merchant_name', models.CharField(max_length=50)),
                ('account_number', models.IntegerField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='bangazonapp.Customer')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bangazonapp.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bangazonapp.Product')),
            ],
            options={
                'verbose_name': 'line_item',
                'verbose_name_plural': 'line_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='line_items',
            field=models.ManyToManyField(through='bangazonapp.OrderProduct', to='bangazonapp.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment', to='bangazonapp.Payment'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_favorites', to='bangazonapp.Customer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='seller_favorites', to='bangazonapp.Customer')),
            ],
            options={
                'verbose_name': 'favorite',
                'verbose_name_plural': 'favorites',
            },
        ),
        migrations.CreateModel(
            name='CustomerLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customerlikes', to='bangazonapp.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customerlikes', to='bangazonapp.Product')),
            ],
            options={
                'verbose_name': 'customer like',
                'verbose_name_plural': 'customer likes',
            },
        ),
    ]
