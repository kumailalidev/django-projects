from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user


class PublishedManager(models.Manager):
    """
    Custom model manager, returns notes only with 'PUBLISHED' status
    and not archived.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=Note.Status.PUBLISHED)
            .filter(archived=False)
        )


class Tag(models.Model):
    """
    Tag model
    """

    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    # overriding save method to automatically generate slug
    def save(self, *args, **kwargs):
        # convert tag name into lowercase
        self.name = self.name.lower()

        # automatically generate the slug from the name
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Note model
    """

    # choices for status field
    class Status(models.TextChoices):
        DRAFT = ("DF", "Draft")
        PUBLISHED = ("PB", "Published")

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=150)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)
    pinned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # model managers
    objects = models.Manager()  # default
    published = PublishedManager()

    # overriding save method to assign current logged in user automatically
    def save(self, *args, **kwargs):
        if self.user_id == None:
            self.user = get_user(self)  # assign the current logged-in user
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
