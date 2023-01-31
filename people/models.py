from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,    
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet

@register_snippet
class Rank_Class(models.Model, index.Indexed):
    rank = models.CharField("Pangkat", max_length=100)
    category = models.CharField("Golongan dan Ruang", max_length=5)

    panels = [
        FieldPanel("rank"),
        FieldPanel("category"),
    ]

    search_fields = [
        index.SearchField("rank"),
        index.SearchField("category"),
    ]

    def __str__(self):
        return "{} {}".format(self.rank, self.category)

    class Meta:
        verbose_name_plural = "Pangkat, Golongan, dan Ruang"
        verbose_name = "Pangkat, Golongan, dan Ruang"

@register_snippet
class Position(models.Model, index.Indexed):
    position = models.CharField("Jabatan", max_length=100)

    panels = [
        FieldPanel("position"),
    ]

    search_fields = [
        index.SearchField("position"),
    ]

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = "Jabatan"
        verbose_name_plural = "Jabatan"

@register_snippet
class Person(
    DraftStateMixin,
    RevisionMixin,    
    PreviewableMixin,    
    index.Indexed,
    ClusterableModel,
):
    name = models.CharField("Nama", max_length=250)
    rank_class = models.ForeignKey(
        Rank_Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pangkat dan Golongan",
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Jabatan",
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("rank_class"),
                        FieldPanel("position"),
                    ]
                )
            ]
        ),
        ImageChooserPanel("image")
    ]

    search_fields = [
        index.SearchField("name"),
        index.SearchField("position"),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition('fill-75x75').img_tag()
        except:
            return ""

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Individu"
        verbose_name_plural = "Anggota"