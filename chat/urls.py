from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name= "home"),
    path('new/', views.new, name= "new"),
    path('profile/', views.profile, name= "profile"),
    path('message/<int:mid>', views.message, name= "message"),
    path('<str:username>/', views.user, name= "user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

