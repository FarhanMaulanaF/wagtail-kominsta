# Generated by Django 4.1.5 on 2023-01-23 04:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('people', '0001_initial'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='person',
            field=models.ForeignKey(blank=True, help_text='Pilih pihak yang ingin ditampilkan.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.person', verbose_name='Pimpinan'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote',
            field=wagtail.fields.RichTextField(blank=True, help_text='Tuliskan kata-kata yang menginspirasi.', null=True, verbose_name='Kata Inspiratif'),
        ),
        migrations.CreateModel(
            name='HomePageCarouselImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('carousel_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Gambar Carousel')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_images', to='home.homepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
