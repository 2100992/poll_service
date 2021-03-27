from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid

# Create your models here.


class Poll(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    start_date = models.DateField(editable=False)
    finish_date = models.DateField()


class Query(models.Model):
    TEXT = 'TXT'
    CHECK = 'CHK'
    RADIO = 'RDO'

    QUERY_TYPE_CHOICES = [
        (TEXT, 'Text response'),
        (CHECK, 'Choice of one option'),
        (RADIO, 'Choice of several options')
    ]

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    body = models.TextField()
    type = models.CharField(
        max_length=3,
        choices=QUERY_TYPE_CHOICES,
        default=TEXT
    )
    response_options = JSONField(
        null=True,
        blank=True,
        default=None,
    )
    required = models.BooleanField(
        default=False
    )


class Person(models.Model):
    uuid = models.CharField(
        max_length=36,
        unique=True
    )
    name = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        default=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())


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
    response = JSONField()
