from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article-column/$',views.article_column,name="article_column"),
    url(r'^rename-column/$',views.rename_article_column,name="rename_article_column"),
    url(r'^delete-column/$',views.delete_article_column,name="delete_article_column"),
    url(r'^article-post/$',views.article_post,name="article_post"),
    url(r'^article-list/$',views.article_list,name="article_list"),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.article_detail,name="article_detail"),
    url(r'^delete-article/$',views.delete_article,name="delete_article"),
    # url(r'^edit-article/$',views.redit_article,name="redit_article"),
    url(r'^redit-article/(?P<article_id>\d+)/$',views.redit_article,name="redit_article"),
    url(r'^list-article-titles/$',views.article_titles,name="article_titles"),
    url(r'^author-articles/(?P<username>[-\w]+)/$',views.article_titles,name="author_articles"),
    url(r'^list-article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.list_article_detail,name="list_article_detail"),
    url(r'^like-article/$',views.like_article,name="like_article"),#用户文章点赞
    url(r'^del-comment/$',views.del_comment,name="del_comment"),
    url(r'^reply-comment/$',views.reply_comment,name="reply_comment"),
    url(r'^article-tag/$',views.article_tag,name="article_tag"),
]