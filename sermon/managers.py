from django.db.models import Manager
import datetime


class PublishedManager(Manager):
    """Returns published sermons that are not in the future."""

    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published=True, publish_on__lte=datetime.datetime.now())