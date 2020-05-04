from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')


admin.site.register(Article, ArticleAdmin)
admin.site.site_header = 'Nilo Admin'
