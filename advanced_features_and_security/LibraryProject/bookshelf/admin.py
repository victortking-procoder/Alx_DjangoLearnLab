from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (('Personal Info'), {'fields': ('date_of_birth', 'profile_photo',)}),
    )
    # Add your custom fields to the list_display
    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)
    # Add your custom fields to the add_fieldsets if you use it for user creation
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Personal Info'), {'fields': ('date_of_birth', 'profile_photo',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)