# Сторонние библиотеки
import os
import decimal

def float_to_str(number: float):
    ctx = decimal.Context()
    ctx.prec = 20

    return format(ctx.create_decimal(repr(number)), 'f')


path_to_dir = os.path.dirname(os.path.abspath(__file__))
