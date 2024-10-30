# `KhataBook Admin Dashboard`

    unzip /home/adminkhatadashboard/app.zip
    find /home/adminkhatadashboard -type d -exec chmod 755 {} +
    python manage.py collectstatic
    zip -r project.zip .

[![image](https://github.com/user-attachments/assets/d71d74aa-e305-4876-a116-b4cf3d1a3fbf)](https://adminkhatadashboard.pythonanywhere.com)

```py
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

