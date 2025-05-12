# storage/models.py
from django.db import models
from accounts.models import User
from storage.utils import generate_image_thumbnail, generate_video_thumbnail
import uuid

class Folder(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.owner.email}"

def file_path(instance: "File", file_name: str):
    folder_part = instance.folder.id if instance.folder else "root"
    return f"files/user_{instance.owner.id}/{folder_part}/{file_name}"

def thumbnail_path(instance: "File", file_name: str):
    folder_part = instance.folder.id if instance.folder else "root"
    return f"thumbnails/user_{instance.owner.id}/{folder_part}/{file_name}"

class File(models.Model):

    FILE_TYPE = (
        ("Image", "Image"),
        ("Video", "Video"),
    )
    
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=thumbnail_path)
    file = models.FileField(upload_to=file_path)
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=10, choices=FILE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=225, unique=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            self.slug = uuid.uuid4()
            ext = self.file.name.split('.')[-1].lower()
            self.file_type = 'Image' if ext in ['jpg', 'jpeg', 'png'] else (
                'Video' if ext in ['mp4', 'mov', 'avi'] else 'Other'
            )

            if not self.thumbnail:
                if self.file_type == 'Image':
                    self.thumbnail = generate_image_thumbnail(self.file)
                elif self.file_type == 'Video':
                    self.thumbnail = generate_video_thumbnail(self.file)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.folder.title if self.folder else 'root'} - {self.owner.email}"
