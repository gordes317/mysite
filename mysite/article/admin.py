from django.contrib import admin
from .models import ArticleColumn

class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column','user','created',)
    list_filter = ('column',)
    search_fields = ("column", "user")

admin.site.register(ArticleColumn,ArticleColumnAdmin)
