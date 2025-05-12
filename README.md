# 📁 Django File Manager

A minimalist, extensible file manager built with Django and DRF, supporting folder nesting, file uploads, renaming, deletion, and direct access via slugs. Designed for both backend flexibility and frontend clarity.

---

## 🚀 Features

* Folder-based file organization (with nesting)
* Breadcrumb navigation for folder hierarchy tracking
* File upload with thumbnail support
* Slug-based file access (`/files/<slug>/`)
* Rename/Delete folders and files
* View file metadata
* Folder/file-level upload and creation
* Client + server-side validations (size, mime-type)

---

## 🛠 Tech Stack

* Django 4+
* Django REST Framework
* HTML/JS frontend (template-based)

---

## 🧱 Project Structure

```bash
├── accounts/         
├── core/           
├── static/
│   └── css/style.css      
├── storage/          
├── templates/
│   └── accounts/
│       └── login.html
│       └── register.html
│   └── storage/
│       └── dashboard.html
│   └── base.html
└── ...
```

---

## 🔧 Setup

```bash
git clone <repo-url>
cd <project>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📤 Upload Restrictions

* **Client-side validation** using `/api/storage/upload-permission/`
* **Server-side enforcement** via MIME type + file size check

Default (editable in backend):

* Images: max 10MB
* Videos: max 50MB

---

## 🔗 Slug-based File Access

Each file gets a unique slug (e.g., `324453c6-a89a-427e-bf59-9417f54633fc`) at creation.

**URL:** `api/storage/files/<slug>/` serves the file.
**URL:** `api/storage/thumbnails/<slug>/` serves the thumbnail.

---

## 🔐 Auth

* No token needed (session-based auth)
* Login/Register/Logout with Django forms

---

## 📄 License

MIT

---

## 👤 Author

Made with ❤️ by \[Abolfazl Jelodar]
