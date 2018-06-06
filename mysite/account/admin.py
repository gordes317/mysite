from django.contrib import admin
from .models import UserProfle,UserInfo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','birth','phone',)
    list_filter = ('phone',)

admin.site.register(UserProfle,UserProfileAdmin)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user','school','company','address','aboutme',)
    list_filter = ('school','company','profession')
    search_fields = ('user',)


admin.site.register(UserInfo,UserInfoAdmin)

# Register your models here.
