from django.contrib import admin
from utm_tags.models import UTMVisit


class UTMVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'source', 'campaign', 'timestamp')
    search_fields = ('source', 'medium', 'term', 'content')
    list_filter = ('source', 'medium', 'timestamp')
    readonly_fields = ('timestamp',)


admin.site.register(UTMVisit, UTMVisitAdmin)
