from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'sex', 'avatar',)
    list_filter = ('sex', )


admin.site.register(User, UserAdmin)
