from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class TextDetails(models.Model):
    """
    Text content, type, and attributes.
    """
    REMINDER = 'FR'
    CHEERLEADING = 'SO'
    BCI = 'JR'
    INFO = 'SR'
    UNASSIGNED = 'GR'
    TEXT_CHOICES = [
        (REMINDER, 'Reminder'),
        (CHEERLEADING, 'Cheerleading'),
        (BCI, 'BCI'),
        (INFO, 'Informational'),
        (UNASSIGNED, 'Unassigned'),
    ]

    id = models.AutoField(primary_key = True)
    text_type = models.CharField(_("Text Type"), max_length = 25,
        choices = TEXT_CHOICES, default = UNASSIGNED)
    body = models.TextField(_("Text Body"), unique = True)
    n_chars = models.PositiveIntegerField(_("Text Length"), null = True, blank = True)
    created = models.DateTimeField(_("Created Datetime"), auto_now_add = True)

    class Meta:
        verbose_name = "Text Details"
        verbose_name_plural = "Text Details"

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        if not self.n_chars:
            self.n_chars = len( [word.split() for word in self.body] )
        super().save()


"""
extras to include:

    def get_absolute_url(self):
        Return absolute URL to the TextDetails Detail page.
        return reverse('texts:detail', kwargs={"slug": self.slug})

# THESE ARE MEANT FOR A TEXTSMANAGER
    def get_text_content(self, pk):
        
        Return text content of a single text by primary key.
        
        pass

    def get_random_text_type(self, type, n = 1):
        
        Return random text(s) of a given type.
        
        pass

    def get_random_text_len(self, len, n = 1):
        
        Return random text(s) of given len OR ABOVE.
        
        pass

"""

