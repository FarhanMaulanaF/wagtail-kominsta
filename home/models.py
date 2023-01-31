from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    InlinePanel, 
    FieldPanel, 
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from people.models import Person

# section untuk carousel
class HomePageCarouselImages(Orderable):
    # diantara 1 dan 5 gambar untuk homepage carousel
    page = ParentalKey("HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Gambar Carousel",
    )

    panels = [
        ImageChooserPanel("carousel_image"),
    ]

# section untuk halaman home
class HomePage(Page): 
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pimpinan",
        help_text=("Pilih pihak yang ingin ditampilkan.")
    )

    quote = RichTextField(
        null=True,
        blank=True,
        verbose_name="Kata Inspiratif",
        help_text=("Tuliskan kata-kata yang menginspirasi.")
    )

    featured_section_title = models.CharField(
        blank=True, max_length=255, help_text="Judul untuk ditampilkan pada bagian tambahan"
    )
    featured_section = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bagian tambahan",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Gambar "),
        ], heading="PENGATURAN CAROUSEL"),
        
        MultiFieldPanel([
            SnippetChooserPanel("person"),
            FieldPanel("quote", classname="full"),
        ], heading="PENGATURAN PROFIL"),

        MultiFieldPanel([
            FieldPanel("featured_section_title"),
            FieldPanel("featured_section"),
        ], heading="PENGATURAN BAGIAN TAMBAHAN"),
    ]
