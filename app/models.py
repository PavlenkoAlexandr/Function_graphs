from django.db import models
from django.utils.safestring import mark_safe
import io
from datetime import timedelta, datetime
import math
import matplotlib.pyplot as plt
from base64 import b64encode

allowed_names = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}


def evaluate(expression):

    code = compile(expression, "<string>", "eval")

    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, allowed_names)


def get_graph_binary(func, interval, dt):

    start = datetime.now() - timedelta(days=int(interval))
    t = list()
    y = list()

    while start <= datetime.now():
        t.append(start.timestamp())
        start += timedelta(hours=int(dt))

    for _ in t:
        allowed_names['t'] = _
        y.append(evaluate(func))

    try:
        plt.xlabel("t")
        plt.ylabel("y")
        plt.grid()
        plt.plot(t, y, 'o-y')
        binary = io.BytesIO()
        plt.savefig(binary)
        graph_binary=binary.getvalue()
        return graph_binary
    except SyntaxError:
        raise SyntaxError("Invalid expression.")
    except (NameError, ValueError) as err:
        raise err


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
            self.graph_binary = get_graph_binary(func=self.func, interval=self.interval, dt=self.step)
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