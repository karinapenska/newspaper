from django.contrib import admin
from .models import Category
from .models import Favourites
from .models import Article
from .models import Like
from .models import Comment
from .models import Profile
admin.site.register(Category)
admin.site.register(Favourites)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)


# Register your models here.
