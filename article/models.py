from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    dob = models.DateField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    categories = models.ManyToManyField('Category', through='Favourites')
    likes = models.ManyToManyField('Article', through='Like')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    CATEGORIES_OPTIONS= (
        ('Sport','sport'),
        ('World','world'),
        ('Covid','covid'),
        ('Business','business'),
    )
    category_name = models.CharField(max_length=200, choices=CATEGORIES_OPTIONS)
    users = models.ManyToManyField('Profile', through='Favourites')
    def __str__(self):
        return self.category_name


class Favourites(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.category.category_name


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=20000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField('Profile', through='Like')

    def __str__(self):
        return self.title

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.IntegerField()