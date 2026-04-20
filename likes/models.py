from django.db import models
from storefront import settings 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class LikedItem(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()


"""
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

other models:
class Post(models.Model):
    title = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=200)

    
Step 3: Create comments
post = Post.objects.first()
comment = Comment.objects.create(
    content_object=post,
    text="Nice post!"
)


OR for a product:

product = Product.objects.first()
comment = Comment.objects.create(
    content_object=product,
    text="Great quality!"
)
"""