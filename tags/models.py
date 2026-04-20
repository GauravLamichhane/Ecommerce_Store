from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
  def get_tags_for(self, obj_type, obj_id):
    """
      Give me the ContentType row that represents the Product model.”

      Internally this points to a row like:

      app_label = store
      model = product

    """
    content_type = ContentType.objects.get_for_model(obj_type)
    # \ = continuation on next line
    """
    .filter(
      content_type = content_type,
      object_id = 1

    This literally means:

    Give me all TaggedItem rows where

    content_type == Product
    AND
    object_id == 1

    In plain English:

    Give me all tags applied to Product with id = 1

    That’s it.
    """
    return TaggedItem.objects \
    .select_related('tag') \
    .filter(
      content_type = content_type,
      object_id = obj_id
    )
  

class Tag(models.Model):
  label = models.CharField(max_length=255)
  def __str__(self):
    return self.label

class TaggedItem(models.Model):
  objects = TaggedItemManager()
  # what tag applied to what object
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
 