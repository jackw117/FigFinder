from django.contrib import admin

from .models import Search, Websites, Details, Entry

admin.site.register(Search)
admin.site.register(Websites)
admin.site.register(Details)
admin.site.register(Entry)