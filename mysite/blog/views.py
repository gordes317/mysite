from django.shortcuts import render,get_object_or_404
from .models import BlogArticles

def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request,"blog/titles.html",{"blogs":blogs})

def blog_article(request,atricle_id):
    article = get_object_or_404(BlogArticles,id=atricle_id)
    pub = article.publish
    return render(request, "blog/content.html",{"article":article,"publish":pub})
# Create your views here.
