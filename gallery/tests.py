from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image
import os
from PIL import Image as PILImage
import io


class ImageDeletionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a test image
        image = PILImage.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        self.uploaded_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_file_deleted_when_model_deleted(self):
        # Create an image instance
        image = Image.objects.create(
            title='Test Image',
            image=self.uploaded_file,
            user=self.user
        )
        
        # Store the file path
        file_path = image.image.path
        
        # Verify file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Delete the image instance
        image.delete()
        
        # Verify file is deleted
        self.assertFalse(os.path.exists(file_path))
    
    def test_old_file_deleted_when_image_updated(self):
        # Create an image instance
        image = Image.objects.create(
            title='Test Image',
            image=self.uploaded_file,
            user=self.user
        )
        
        # Store the original file path
        old_file_path = image.image.path
        
        # Create a new test image
        new_image = PILImage.new('RGB', (100, 100), color='blue')
        new_image_io = io.BytesIO()
        new_image.save(new_image_io, format='JPEG')
        new_image_io.seek(0)
        
        new_uploaded_file = SimpleUploadedFile(
            name='new_test_image.jpg',
            content=new_image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        # Update the image
        image.image = new_uploaded_file
        image.save()
        
        # Verify old file is deleted
        self.assertFalse(os.path.exists(old_file_path))
        
        # Verify new file exists
        self.assertTrue(os.path.exists(image.image.path))
        
        # Clean up
        image.delete()