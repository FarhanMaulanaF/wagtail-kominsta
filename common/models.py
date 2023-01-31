from django.db import models
from wagtail.models import Page, Collection
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from common.blocks import BaseStreamBlock

# section untuk standard page
class StandardPage(Page):
    introduction = models.TextField(help_text="Teks untuk mendeskripsikan halaman ini.", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Mode landscape saja; Lebar horizontal antara 1000px dan 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]  

# section untuk halaman galeri
class GalleryPage(Page):
    introduction = models.TextField(help_text="Teks untuk mendeskripsikan halaman ini.", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Mode landscape saja; Lebar horizontal antara 1000px dan 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Pilih koleksi gambar untuk ditampilkan pada halaman ini.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("collection"),
    ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = []