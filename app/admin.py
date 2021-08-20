from django.contrib import admin

from app.models import Graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    fields = ('func', 'interval', 'step')
    list_display = ('func', 'graph_binary_tag', 'interval', 'step', 'processing_date')

    readonly_fields = ('graph_binary', 'graph_binary_tag')