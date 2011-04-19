from datetime import datetime
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from markup_mixin.models import MarkupMixin

from sermon.managers import PublishedManager

''' You can import a person model from wherever '''

class Speaker(models.Model):
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    try:
        from committees.models import Person
        person = models.ForeignKey(Person)
    except:
        person = models.CharField(_('Person'), max_length=100)
    
    @property
    def name(self):
        try:
            return self.person.full_name
        except:
            return self.person

    def __unicode__(self):
        if self.person.title:
            return self.person.title + " " + self.name
        else:
            return self.name

    def get_absolute_url(self):
        args=[self.slug]
        return reverse('sr-speaker-detail', args=args)


class Reading(models.Model):
    source = models.CharField(_('source'), max_length=255)
    text = models.TextField(_('text'))

    def __unicode__(self):
        return self.source


class Sermon(MarkupMixin, TimeStampedModel):
    speaker = models.ForeignKey(Speaker)
    date = models.DateField()
    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), unique=True)
    readings = models.ManyToManyField(Reading, blank=True, null=True)
    mp3file = models.FileField(upload_to="sermons/", blank=True, null=True, help_text=_("This should be a low quality version (preferably 18kbps), because it will be used for the Flash player."))
    largemp3file = models.FileField(upload_to="sermons/", null=True, blank=True,help_text=_("Optional. Preferably a 64kps version."))
    body = models.TextField(_('Body'))
    rendered_content = models.TextField(_('Rendered content'), blank=True, null=True, editable=False)
    published = models.BooleanField(_('published'), default=True)
    publish_on = models.DateTimeField()
    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = _('sermon')
        verbose_name_plural = _('sermons')
        get_latest_by = 'publish_on'

    class MarkupOptions:
        source_field = 'body'
        rendered_field = 'rendered_content'
    
    def __unicode__(self):
        return u'%s - %s - %s' % (self.date.isoformat(), self.title, self.speaker.name)

    def get_absolute_url(self):
        args=[self.date.year, self.slug]
        return reverse('sr-sermon-detail', args=args)

    def get_next_sermon(self):
        """Determines the next live sermon"""

        if not self._next:
            try:
                qs = Sermon.objects.all().exclude(id__exact=self.id)
                sermon= qs.filter(date__gte=self.date).order_by('-date')[0]
            except (Article.DoesNotExist, IndexError):
                article = None
            self._next = article

        return self._next

    def get_previous_article(self):
        """Determines the previous live article"""

        if not self._next:
            try:
                qs = Sermon.objects.all().exclude(id__exact=self.id)
                sermon= qs.filter(date__lte=self.date).order_by('-date')[0]
            except (Article.DoesNotExist, IndexError):
                article = None
            self._previous = article

        return self._next

