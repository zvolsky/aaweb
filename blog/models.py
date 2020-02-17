from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class BlogPage(Page):
    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

    class Meta:
        verbose_name = _("Blog page")
        verbose_name_plural = _("Blog pages")


class PostPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    class Meta:
        verbose_name = _("Blog post page")
        verbose_name_plural = _("Blog post pages")
