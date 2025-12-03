from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from partnership import views  # Import your login_view

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Root URL shows login page
    path('', views.login_view, name='login'),

    # Include other partnership URLs (optional for dashboard, signup, API, etc.)
    path('partnership/', include('partnership.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
