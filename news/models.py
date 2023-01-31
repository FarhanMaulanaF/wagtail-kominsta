from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.shortcuts import redirect, render
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from common.blocks import BaseStreamBlock
from people.models import Person


class NewsPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        "NewsPage", related_name="news_person_relationship", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "people.Person", related_name="person_news_relationship", on_delete=models.CASCADE
    )
    panels = [FieldPanel("person")]

class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "NewsPage", related_name="tagged_items", on_delete=models.CASCADE
    )

class NewsCarouselImages(Orderable):
    page = ParentalKey("NewsPage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Gambar Carousel",
    )

    panels = [
        ImageChooserPanel("carousel_image"),
    ]

class NewsPage(Page):
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
    subtitle = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    date_published = models.DateTimeField("Tanggal dan waktu artikel diterbitkan.", blank=True, null=True)
    show_writer = models.BooleanField(default=False, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("date_published"),
        InlinePanel(
            "news_person_relationship",
            heading="Authors",
            label="Author",
            panels=None,
            min_num=1,
        ),
        FieldPanel(
            "show_writer",
            help_text="Tampilkan penulis pada halaman berita.",
        ),
        InlinePanel("carousel_images", max_num=5, min_num=1, label="Gambar "),
        FieldPanel("tags"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    def authors(self):
        return Person.objects.filter(live=True, person_news_relationship__page=self)

    @property
    def get_tags(self):
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags

    parent_page_types = ["NewsIndexPage"]

    subpage_types = []


class NewsIndexPage(RoutablePageMixin, Page):
    introduction = models.TextField(help_text="Teks untuk mendeskripsikan halaman ini.", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Mode landscape saja; Lebar horizontal antara 1000px dan 3000px.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    subpage_types = ["NewsPage"]

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(NewsIndexPage, self).get_context(request)
        context["posts"] = (
            NewsPage.objects.descendant_of(self).live().order_by("-date_published")
        )
        return context

    @route(r"^tags/$", name="tag_archive")
    @route(r"^tags/([\w-]+)/$", name="tag_archive")
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'Tidak ada postingan berita yang diberi tag "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {"tag": tag, "posts": posts}
        return render(request, "news/news_index_page.html", context)

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    def get_posts(self, tag=None):
        posts = NewsPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
