from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from enum import Enum


class SourceStates(Enum):
    PENDING = 'pending'
    CRAWLED = 'crawled'
    READY = 'ready'
    REJECTED = 'rejected'
    FAILED = 'failed'
    CONTENT_COMPLETE = 'content_complete'
    INDEXED = 'indexed'


class AllUrlStates(Enum):
    PENDING = 'pending'
    PARSED = 'processed'
    FAILED = 'failed'
    INDEXED = 'indexed'


class ArticleStates(Enum):
    PENDING = 'pending'
    PARSED = 'parsed'
    EXTRACTED = 'extracted'


class Source(models.Model):
    domain_name = models.URLField()
    state = FSMField(default=SourceStates.PENDING.value, db_index=True)
    trusted_source = models.BooleanField(default=False)
    last_time_crawled = models.DateTimeField(null=True, blank=True)
    last_error_message = models.TextField(default='', blank=True)

    @transition(
        field=state,
        source=SourceStates.PENDING.value,
        target=SourceStates.READY.value,
    )
    def ready(self):
        pass

    @transition(
        field=state,
        source=SourceStates.READY.value,
        target=SourceStates.CRAWLED.value
    )
    def crawl(self):
        self.last_time_crawled = timezone.now()

    @transition(
        field=state,
        source='*',
        target=SourceStates.REJECTED.value
    )
    def reject(self):
        pass

    @transition(
        field=state,
        source='*',
        target=SourceStates.FAILED.value,
        custom=dict(admin=False)
    )
    def fail(self, error=''):
        self.last_error_message = error

    @transition(
        field=state,
        source=SourceStates.CRAWLED.value,
        target=SourceStates.CONTENT_COMPLETE.value
    )
    def complete(self):
        pass

    @transition(
        field=state,
        source=SourceStates.CONTENT_COMPLETE.value,
        target=SourceStates.INDEXED.value
    )
    def index(self):
        pass

    def __str__(self):
        return '[domain_name: {}] [state: {}] [trusted_source: {}]'.format(
            self.domain_name, self.state, self.trusted_source
        )


class AllUrl(models.Model):
    source = models.ForeignKey(
        Source,
        related_name='urls',
        related_query_name='url',
        on_delete=models.CASCADE
    )
    url = models.URLField()
    state = FSMField(default=AllUrlStates.PENDING.value, db_index=True)
    html = models.TextField(default='')
    is_article = models.BooleanField(default=True)

    @transition(
        field=state,
        source='*',
        target=AllUrlStates.PARSED.value
    )
    def processed(self):
        pass

    @transition(
        field=state,
        source='*',
        target=AllUrlStates.FAILED.value
    )
    def fail(self):
        pass

    @transition(
        field=state,
        source=AllUrlStates.PARSED.value,
        target=AllUrlStates.INDEXED.value
    )
    def index(self):
        pass

    def __str__(self):
        return self.url


class Article(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    domain_name = models.CharField(max_length=255)
    text = models.TextField(default='')
    keywords = models.TextField(default='')
    authors = models.TextField(default='')
    tags = models.CharField(max_length=255)
    summary = models.TextField(default='')
    links = models.CharField(max_length=255)
    parse_time = models.CharField(max_length=255)
    publish_date = models.DateField()
    state = FSMField(default=ArticleStates.PENDING.value, db_index=True)

    @transition(
        field=state,
        source='*',
        target=ArticleStates.EXTRACTED.value
    )
    def extracted(self):
        pass

    @transition(
        field=state,
        source='*',
        target=ArticleStates.PARSED.value
    )
    def parsed(self):
        pass
