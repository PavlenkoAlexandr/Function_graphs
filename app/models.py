from django.db import models
from django.utils.safestring import mark_safe
from base64 import b64encode
from .tasks import get_graph_binary


class Graph(models.Model):

    func = models.TextField()
    graph_binary = models.BinaryField(blank=True, default=bytes('', 'utf-8'))
    is_error = models.BooleanField(default=False)
    interval = models.IntegerField()
    step = models.IntegerField()
    processing_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.is_error = False
            graph_binary = get_graph_binary.delay(func=self.func, interval=self.interval, dt=self.step)
            self.graph_binary = graph_binary.get()
        except Exception as e:
            self.is_error = True
            self.graph_binary = bytes(str(e), 'utf-8')
        super().save(*args, **kwargs)

    def graph_binary_tag(self):
        if self.is_error:
            return str(self.graph_binary, 'utf8')
        return mark_safe(f'<img src = "data: image/png; base64, {b64encode(self.graph_binary).decode("utf8")}" width="640" height="480">')

    graph_binary_tag.short_description = 'Image'
    graph_binary_tag.allow_tags = True
