from django.conf.urls.defaults import *
from django.conf import settings

from sermon import views

urlpatterns = patterns('sermon.views',
    url (r'^$', view=views.index, name='sr-index', ),
    url (r'^(?P<year>[\d]+)/(?P<slug>[-\w]+)/$', view=views.sermon_detail, name='sr-sermon-detail', ),
    url (r'^(?P<slug>[-\w]+)/$', view=views.speaker_detail, name='sr-speaker-detail', ),
)
