from rest_framework import serializers
from storage.models import Folder, File

class FolderSerializer(serializers.ModelSerializer):
    files_count = serializers.SerializerMethodField()
    subfolders_count = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['id', 'title', 'parent', 'files_count', 'subfolders_count']

    def get_files_count(self, obj):
        return obj.files.count()

    def get_subfolders_count(self, obj):
        return obj.subfolders.count()

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'id',
            'title',
            'file',
            'thumbnail',
            'file_type',
            'size',
            'folder',
            'created_at',
            'slug'
        ]
        read_only_fields = ['thumbnail', 'file_type', 'size', 'created_at', 'slug']

    def validate_file(self, file):
        import mimetypes
        from defaults import VALID_MIME_TYPES, DEFAULT_MIME_TYPE_MAX_SIZE

        mime_value, _ = mimetypes.guess_type(file.name)
        valid_types = VALID_MIME_TYPES['Image'] + VALID_MIME_TYPES['Video']

        if mime_value not in valid_types:
            raise serializers.ValidationError("Unsupported file type.")
        
        mime_type = "Image" if mime_value.startswith("image/") else "Video"
        if file.size > DEFAULT_MIME_TYPE_MAX_SIZE[mime_type]:
            raise serializers.ValidationError("File is too large.")

        return file
