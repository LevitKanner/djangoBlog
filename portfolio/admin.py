from django.contrib import admin
from .models import Personal, Language

# Register your models here.
class LanguageInline(admin.TabularInline):
    model = Language
    
@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Info', {'fields': ['name']}),
        ('Links', {'fields': ['twitter', 'email', 'github']})
    ]
    list_display = ('name', 'twitter', 'email', 'github')
    inlines = [LanguageInline]
    

    
# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     class Meta:
#         ordering = ('name',)