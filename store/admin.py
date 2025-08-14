from django.contrib import admin
from .models import Category ,Customer,Items,Order,Profile
from django.contrib.auth.models import User



admin.site.register(Category)
admin.site.register(Items) 
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(Order)

#Mix profile info and userinfo
class ProfileInline(admin.StackedInline):
    model=Profile

#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model=User
    field=["username","first_name","last_name","email"]
    inlines=[ProfileInline]

#Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User,UserAdmin)