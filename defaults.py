VALID_MIME_TYPES = {
    "Image": [
        "image/jpg",
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    ],
    "Video": [
        "video/mp4",
        "video/x-msvideo",  # avi
        "video/quicktime",  # mov
        "video/x-matroska", # mkv
    ]
}

DEFAULT_MIME_TYPE_MAX_SIZE = {
    "Image": 10 * 1024 * 1024,
    "Video": 50 * 1024 * 1024,
}