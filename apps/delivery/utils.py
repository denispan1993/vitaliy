# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def parsing(value, key, ):
    values = value.split('{{ id }}', )
    n = 0
    cycle = 0
    value = ''
    part_count = len(values, )
    if part_count > 0:
        for value_part in values[::2]:  # перечисляем все куски с шагом 2
            n += 2
            cycle += 1
            print 'n: ', n, ' cycle: ', cycle
            value = '%s%s%s%s' % (value, value_part, key, values[n], )
    return value
