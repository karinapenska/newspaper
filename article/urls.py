from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('category/<str:category>', views.categories, name="categories"),
    path('profile', views.profile, name="profile"),
    path('profile/delete', views.deletePic, name="profile_delete"),
    path('<int:article_id>', views.article, name='article'),
    path('<int:article_id>/like', views.like_article, name="like_article"),
    path('<int:article_id>/comment/', views.comment_article, name='comment_article'),
    path('<int:article_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:article_id>/update/', views.update_comment, name='update_comment')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


