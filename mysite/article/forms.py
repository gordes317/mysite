from .models import ArticlePost,ArticleColumn,Replying
from django import forms
from .models import Comment
from .models import ArticleTag

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Replying
        fields = ("content",)

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields =("tag",)