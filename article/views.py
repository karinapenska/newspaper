from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import sys
import os
from django.db.models import F
from django.db import connection
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


cursor = connection.cursor()
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    articles_list = Article.objects.order_by('id')
    articles_sorted=Article.objects.none()


    if request.user.is_authenticated:

        user=Profile.objects.filter(user=request.user)

        favourites=Favourites.objects.filter(user=user[0])
        for favourite in favourites:
            articles_sorted= articles_sorted | articles_list.filter(category_id=favourite.category_id)
            articles_sorted=articles_sorted.order_by('id')


    else:
        articles_sorted=articles_list

    context = {'articles_list': articles_sorted.reverse()}

    return render(request, 'article/home.html', context)



def categories(request,category):
    articles_list = Article.objects.order_by('id')
    articles_sorted=articles_list.filter(category__category_name=category)

    context = {'articles_list': articles_sorted.reverse()}

    return render(request, 'article/home.html', context)


def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        form1 = ProfileUpdateForm(request.POST)
        if form.is_valid():
            if form1.is_valid():
                form.save(commit=False)
                form1.save(commit=False)
                user=form.save()
                #email_subject = 'Welcome to News Articles Website!'
                #email_body = 'Welcome to News Articles Website! Thank you for registering.'
                #email = EmailMessage(
                    #email_subject,
                    #email_body,
                    #'noreply@semycolon.com',
                    #['email'],
                #)
                #email.send(fail_silently=False)
                p = Profile(user=user,dob=request.POST['dob'])

                p.save()
                print("sc1")
                for category in request.POST.getlist('categories'):
                    print(category)
                print(request.POST.getlist('categories'))
                request.POST['email']
                p.categories.set(request.POST.getlist('categories'))

                print(p)




                print('success')
                return redirect('login')

            #username = form.cleaned_data.get('username')
            #dob = form.cleaned_data['date_of_birth']
            #messages.success(request, f'Account registered. You are able to login now.')

            else:
                print("zjebalo sie")
        else:
            print("zjebalo sie")

    else:
        form = UserRegisterForm()
        form1 = ProfileUpdateForm()
    return render(request, 'article/register.html', {'form': form,'form1':form1})

@login_required
def profile(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }
    return render(request, 'article/profile.html', context)

@csrf_exempt
def deletePic(request):
    if request.method == 'DELETE':
        userProfile=request.user.profile
        pictureName=userProfile.image
        userProfile.image="default.jpg"
        print("chuj")
        print(pictureName)
        os.remove("media/"+str(pictureName))
        userProfile.save()
        return JsonResponse(200, safe=False)
    else:
        return JsonResponse(400, safe=False)

def article(request, article_id):
    selected_article = get_object_or_404(Article, pk=article_id)
    count=0
    like=False
    comments=Comment.objects.filter(article=selected_article)
    if request.user.is_authenticated:
        user=Profile.objects.filter(user=request.user)
        num_results = Like.objects.filter(article=selected_article, user=user[0]).count()



        if num_results>0:
            like=True

    for l in Like.objects.filter(article=selected_article):
        count+=1

    context = {'article': selected_article,'count':str(count),'like':like,'comments':comments,}
    return render(request, 'article/article.html', context)

@login_required
@csrf_exempt
def like_article(request, article_id):

    if request.method == "LIKE":

        user=Profile.objects.filter(user=request.user)
        selected_article = get_object_or_404(Article, pk=article_id)

        num_results = Like.objects.filter(article=selected_article, user=user[0]).count()


        if num_results>0:
            Like.objects.filter(article = selected_article, user=user[0]).delete()
            return JsonResponse(200, safe=False)

        else:
            like=Like(article = selected_article,user=user[0])
            like.save()
            return JsonResponse(200, safe=False)


    else:
        return "There was an error while liking an article"
@csrf_exempt
def comment_article(request, article_id):
    if request.method == "POST":
        comment_text = request.POST.get('comment_text')
        selected_article = get_object_or_404(Article, pk=article_id)
        if request.user.is_authenticated:
            current_username = request.user.profile

            comment_instance = Comment(article=selected_article,
                                                  user=current_username,
                                                  content= comment_text,
                                                    parent=0
                                                  )
            comment_instance.save()

        return JsonResponse(200, safe=False)
    else:
        return "There was an error while posting your comment"

@csrf_exempt
def delete_comment(request, article_id):
    if request.method == 'POST':
        deleted_comment_id = request.POST.get('delete_id')
        Comment.objects.filter(id=deleted_comment_id).delete()
        return JsonResponse(200, safe=False)
    else:
        return "There was an error while deleting your comment"

@csrf_exempt
def update_comment(request, article_id):
    if request.method == 'POST':
        updated_comment_id = request.POST.get('update_id')
        updated_comment_text = request.POST.get('update_text')

        selected_comment = Comment.objects.filter(id=updated_comment_id)
        selected_comment.update(content = updated_comment_text)

        return JsonResponse(200, safe=False)
    else:
        return "There was an error while updating your comment"

