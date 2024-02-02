from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

class Translations(models.Model):
    id = models.AutoField(primary_key=True)
 
class Article(models.Model):
    translation_parent = models.ForeignKey(Translations, on_delete=models.CASCADE, related_name='translation_objects', blank=True)
    language = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    body = models.JSONField()
    slug = models.SlugField(blank=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('language', 'title',)

@receiver(pre_save, sender=Article)
def add_article_slug(sender, instance, *args, **kwargs):
    instance.slug = instance.title.lower().replace(" ", "-").replace(",", "")


