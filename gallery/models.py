from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os


class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(
        upload_to='gallery/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title or f"Image {self.id}"


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    """Delete the image file from filesystem when the Image model instance is deleted"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Image)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Delete old image file when updating with a new image"""
    if not instance.pk:
        return False

    try:
        old_image = Image.objects.get(pk=instance.pk).image
    except Image.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
