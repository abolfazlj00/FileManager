# storage/views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Folder, File
from .serializers import FolderSerializer, FileSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponseForbidden
from defaults import VALID_MIME_TYPES, DEFAULT_MIME_TYPE_MAX_SIZE

# ──────── Folder List + Create ────────
class FolderListCreateView(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# ──────── Folder Rename ────────
class FolderRenameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            folder = Folder.objects.get(pk=pk, owner=request.user)
        except Folder.DoesNotExist:
            return Response({"detail": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get("title")
        if not title:
            return Response({"detail": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

        folder.title = title
        folder.save(update_fields=["title"])
        return Response({"detail": "Title updated successfully."})
    
# ──────── Folder Delete ────────
class FolderDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

# ──────── File List + Upload ────────
class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = File.objects.filter(
            owner=self.request.user,
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# ──────── File Rename ────────
class FileRenameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            file = File.objects.get(pk=pk, owner=request.user)
        except File.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get("title")
        if not title:
            return Response({"detail": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

        file.title = title
        file.save(update_fields=["title"])
        return Response({"detail": "Title updated successfully."})

# ──────── File Delete ────────
class FileDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

# ──────── Dashboard ────────
@login_required
def dashboard_view(request):
    return render(request, 'storage/dashboard.html')

# ──────── Upload Permissions ────────
@api_view(['GET'])
def upload_permission_view(request):
    return Response(
        data={
            mime_type: {
                "max_size": DEFAULT_MIME_TYPE_MAX_SIZE[mime_type],
                "mime_types": mime_values
            }
            for mime_type, mime_values in VALID_MIME_TYPES.items()
        },
        status=status.HTTP_200_OK
    )

@login_required
def file_view_by_slug(request, slug):
    file_obj = get_object_or_404(File, slug=slug)
    if file_obj.owner == request.user:
        return FileResponse(file_obj.file.open())
    return HttpResponseForbidden(content="Access is denied!")

@login_required
def thumbnail_view_by_slug(request, slug):
    file_obj = get_object_or_404(File, slug=slug)
    if file_obj.owner == request.user:
        return FileResponse(file_obj.thumbnail.open())
    return HttpResponseForbidden(content="Access is denied!")