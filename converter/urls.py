from django.urls import path
from .views import file_upload_view,register,login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload/', file_upload_view, name='file-upload'),

    path('register/', register, name='register'),

    path('login/', login_view, name='login'),
    # path('login/',auth_views.LoginView.as_view(template_name='converter/login.html',redirect_field_name='converter/upload.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'converter/logout.html'), name='logout'),
]

# if settings.DEBUG:  # Serve media files in development only
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)