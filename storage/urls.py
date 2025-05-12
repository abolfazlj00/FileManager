from django.urls import path
from .views import (
    FolderListCreateView, FolderRenameView, FolderDeleteView,
    FileListCreateView, FileRenameView, FileDeleteView, upload_permission_view,
    thumbnail_view_by_slug, file_view_by_slug
)

urlpatterns = [
    path('folders/', FolderListCreateView.as_view(), name='folder-list-create'),
    path('folders/<int:pk>/rename/', FolderRenameView.as_view(), name='folder-rename'),
    path('folders/<int:pk>/', FolderDeleteView.as_view(), name='folder-delete'),

    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:pk>/rename/', FileRenameView.as_view(), name='file-rename'),
    path('files/<int:pk>/', FileDeleteView.as_view(), name='file-delete'),

    path('thumbnails/<str:slug>', thumbnail_view_by_slug),
    path('files/<str:slug>', file_view_by_slug),

    path('upload-permission/', upload_permission_view, name='upload-permission'),
]
