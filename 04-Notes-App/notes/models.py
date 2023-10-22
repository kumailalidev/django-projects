from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
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
