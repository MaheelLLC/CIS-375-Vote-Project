from django.contrib import admin
from .models import Poll, Option

# Register your models here.
class PollAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Poll, PollAdmin)
admin.site.register(Option)