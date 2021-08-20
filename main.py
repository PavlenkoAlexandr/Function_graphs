# import io
# import math
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
#
#
# ALLOWED_NAMES = {
#     k: v for k, v in math.__dict__.items() if not k.startswith("__")
# }
#
#
#
# def evaluate(expression):
#
#     code = compile(expression, "<string>", "eval")
#
#     for name in code.co_names:
#         if name not in ALLOWED_NAMES:
#             raise NameError(f"The use of '{name}' is not allowed")
#
#     return eval(code, {"__builtins__": {}}, ALLOWED_NAMES)
# #
# func = 't**2'
#
# start = -10
# t = list()
# y = list()
#
# while start <= 10:
#     t.append(start)
#     start += 1
#
# for _ in t:
#     ALLOWED_NAMES['t'] = _
#     y.append(evaluate(func))
#
# try:
#     plt.xlabel("t")
#     plt.ylabel("y")
#     plt.grid()
#     plt.plot(y, t, 'o-y')
#     binary = io.BytesIO()
#     plt.savefig(binary)
#     graph_binary = binary.getvalue()
#     plt.show()
# except SyntaxError:
#     print("Invalid expression.")
# except (NameError, ValueError) as err:
#     print(err)
