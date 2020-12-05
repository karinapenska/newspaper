from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from article import views as article_views

urlpatterns = [
    path('', include('article.urls')),
    path('register/', article_views.register, name='register'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='article/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='article/logout.html'), name='logout'),
]