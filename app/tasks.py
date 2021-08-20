import io
from datetime import timedelta, datetime
import math
import matplotlib.pyplot as plt
from celery import shared_task

allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}


def evaluate(expression):

    code = compile(expression, "<string>", "eval")

    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, allowed_names)


@shared_task
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
        graph_binary = binary.getvalue()
        return graph_binary
    except SyntaxError:
        raise SyntaxError("Invalid expression.")
    except (NameError, ValueError) as err:
        raise err
