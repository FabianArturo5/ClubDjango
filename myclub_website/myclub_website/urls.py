from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')), #allow to use aut of django
    path('members/', include('members.urls')),
]

# Configure Admin Titles
admin.site.site_header = "My Club Administration Page"
admin.site.site_title = "Admin Area"
admin.site.index_title = "Welcome to admin area"