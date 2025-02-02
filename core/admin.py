from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Tool, Rental, Payment, Review

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Category)
admin.site.register(Tool)
admin.site.register(Rental)
admin.site.register(Payment)
admin.site.register(Review)
