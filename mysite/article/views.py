from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ArticleColumn,ArticlePost,Comment,Replying,ArticleTag
from django.http import HttpResponse
from .forms import ArticleColumnForm,ArticlePostForm,CommentForm,ReplyForm,ArticleTagForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User

import redis
from django.conf import settings

#链接redis数据库
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
# @login_required(login_url='/account/login/')
# def article_column(request):
#     columns = ArticleColumn.objects.filter(user=request.user)
#     return render(request,"article/column/article_column.html",{"columns":columns})

@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    """添加栏目
    """
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user_id=request.user.id)
        column_form = ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,"column_form":column_form})
    if request.method =="POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            # ArticleColumn.objects.create(user_id=request.user.id,column=column_name)
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')

    if request.method =="POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            # ArticleColumn.objects.create(user_id=request.user.id,column=column_name)
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def rename_article_column(request):
    """编辑文章栏目名称
    """
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def delete_article_column(request):
    """删除文章栏目
    """
    # column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        # line.column = column_name
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    """文章发布
    """
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:

            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        #article_columns = ArticleColumn.objects.filter(user=request.user) 与上一句作用相同
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns})

@login_required(login_url='/account/login/')
def article_list(request):
    """显示文章列表
    """
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list,2)
    page = request.GET.get('page')
    try :
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/column/article_list.html",{"articles":articles,"page":current_page})

@login_required(login_url='/account/login/')
def article_detail(request,id,slug):
    """显示文章内容(后台)
    """
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/column/article_detail.html",{"article":article})

@csrf_exempt
def list_article_detail(request,id,slug):
    """显示文章内容
    """
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    total_views =r.incr("article:{}:views".format(article.id))#记录访问文章的次数
    r.zincrby('article_ranking',article.id,1)

    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    if request.method =="POST":
        comment_form = CommentForm(data=request.POST)
        # comments = Comment.objects.filter(article_id=id)

        # print(request.POST['user_name'])
        # print(request.POST['body'])
        if comment_form.is_valid():
            try:
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.commentator = request.POST['user_name']
                new_comment.body = request.POST['body']
                new_comment.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        return  HttpResponse("3")
    else:
        comment_form = CommentForm()
        artobj=ArticlePost.objects.get(id=id).comments.all()
        rep_id = [ art.id for art in artobj ]
        reply=Replying.objects.filter(reply_id__in=rep_id)
        # reply = Replying.objects.all()

        paginator = Paginator(reply, 5)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            replys = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            replys = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            replys = current_page.object_list
        #return HttpResponse("3")
        return render(request,"article/list/article_detail.html",
                  {"article":article,"total_views":total_views,
                   "most_viewed":most_viewed,"comment_form":comment_form,"page":current_page,"replys":replys})

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def delete_article(request):
    """删除文章
    """
    article_id = request.POST['article_id']
    try:
        line = ArticlePost.objects.get(id=article_id)
        # line.column = column_name
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

@login_required(login_url='/account/login/')
@csrf_exempt

def redit_article(request,article_id):
    """编辑文章
    """
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        return render(request,"article/column/redit_article.html",{"article":article,"article_columns":article_columns,"this_article_form":this_article_form,"this_article_column":this_article_column})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            print(request.POST)
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")

def article_titles(request,username=None):
    """显示文章标题,若没传入作者,则为请求所有作者的文章
    """
    if username:
        user = User.objects.get(username=username)#得到某个用户的对象
        article_title = ArticlePost.objects.filter(author=user)#得到某个用户的文章对象
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()
    paginator = Paginator(article_title,5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request,"article/list/author_article_titles.html",
                      {"userBean":user,"userinfo":userinfo,"articles":articles,"page":current_page})
    else:
        return render(request, "article/list/article_titles.html",
                      {"articles": articles, "page": current_page})

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def like_article(request):
    """文章点赞
    """
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
            else:
                article.users_like.remove(request.user)
            count = article.users_like.count()
            return HttpResponse(count)
        except:
            return HttpResponse("no")

@csrf_exempt
@login_required(login_url='/account/login/')
def del_comment(request):
    """删除评论
    """
    comment_id = request.POST['comment_id']

    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@csrf_exempt
@login_required(login_url='/account/login/')
def reply_comment(request):
    if request.method == "POST":
        Replying.objects.create(content=request.POST['body'],
                                commentator=request.POST['commentator'],
                                repler=request.POST['repler'],
                                reply_id=request.POST['comment_id'])
        # reply_form.save()
        return HttpResponse("1")
    else:
        return HttpResponse("2")

        # return  HttpResponse("3")

@csrf_exempt
@login_required(login_url='/account/login/')
def article_tag(request):
    if request.method =="GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request,'article/tag/tag_list.html',
                      {"article_tags":article_tags,"article_tag_form":article_tag_form,})
    if request.method =="POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                print(request.POST['tag'])
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be save")
        else:
            return HttpResponse("sorry,the form is not vaild.")






