from django.contrib import admin
from .models import ResearchPaper
# Register your models here.
@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'upload_date')
    search_fields = ('title', 'author')
    # list_filter = ('upload_date',)

# admin.site.register(ResearchPaper, ResearchPaperAdmin)