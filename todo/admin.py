from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('completed', 'created_at')

# OR simpler
# admin.site.register(Task)
