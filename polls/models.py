from django.db import models
from django.contrib.postgres.fields import JSONField
import json
import uuid

# Create your models here.


class Poll(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    start_date = models.DateField()
    finish_date = models.DateField()
    queries = models.ManyToManyField(
        'Query',
        related_name='polls'
    )
    order_of_queries = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        return self.title

    @property
    def new_order_of_queries(self):

        # take a list of id's self.queries
        self_query_ids = list(self.queries.all().values_list('id', flat=True))

        # take a list of id's self.order_of_queries
        try:
            order_of_queries = json.loads(self.order_of_queries)
        except Exception:
            order_of_queries = []

        if not isinstance(order_of_queries, list):
            order_of_queries = []

        # check list order_of_queries
        for idx,q_id in enumerate(order_of_queries):
            if q_id not in self_query_ids:
                del(order_of_queries[idx])
        
        # add id to order_of_queries from self.queries
        for query_id in self_query_ids:
            if query_id not in order_of_queries:
                order_of_queries.append(query_id)

        return json.dumps(order_of_queries)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order_of_queries != self.new_order_of_queries:
            self.order_of_queries = self.new_order_of_queries
            self.save()


class Option(models.Model):
    '''
    Possible options for response
    '''
    body = models.CharField(max_length=255)

    def __str__(self):
        return self.body


class Query(models.Model):
    TEXT = 'TXT'
    CHECK = 'CHK'
    RADIO = 'RDO'

    QUERY_TYPE_CHOICES = [
        (TEXT, 'Text response'),
        (CHECK, 'Choice of one option'),
        (RADIO, 'Choice of several options')
    ]
    title = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        default=None,
    )
    body = models.TextField()
    type = models.CharField(
        max_length=3,
        choices=QUERY_TYPE_CHOICES,
        default=TEXT
    )
    is_required = models.BooleanField(
        default=False
    )
    response_options = models.ManyToManyField(
        Option,
        related_name='queries',
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        if self.title:
            return self.title
        return self.body[:140]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Person(models.Model):
    uuid = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        default=''
    )
    name = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        default=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        if self.name:
            return f'{self.uuid} - {self.name}'
        return self.uuid


class Response(models.Model):
    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    body = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None
    )
    selected_options = models.ManyToManyField(
        Option,
        related_name='responses',
    )

    def save(self):
        for option in self.selected_options:
            if option not in self.query.response_options.all():
                self.selected_options.remove(option)
        super().save(*args, **kwargs)
