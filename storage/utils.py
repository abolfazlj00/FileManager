from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile, File
import os
import ffmpeg
import tempfile

def generate_image_thumbnail(image_field, size=(300, 300)):
    image = Image.open(image_field)
    image.thumbnail(size)
    thumb_io = BytesIO()
    image.save(thumb_io, format="jpeg")
    return ContentFile(thumb_io.getvalue(), name="thumbnail.jpeg")

def generate_video_thumbnail(video_field):

    temp_thumb = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_thumb_path = temp_thumb.name

    input_path = video_field.path

    (
        ffmpeg
        .input(input_path, ss=0)
        .filter('scale', 300, -1)
        .output(temp_thumb_path, vframes=1)
        .overwrite_output()
        .run(quiet=True)
    )

    with open(temp_thumb_path, 'rb') as f:
        django_file = File(f, name="thumbnail")

    return django_file