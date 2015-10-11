# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def parsing(value, key, ):
    from re import split
    values = split('{{ id }}', value, )
    n = 0
    cycle = 0
    value = ''
    part_count = len(values, )
    print 'part_count: ', part_count
    if part_count > 1:
        for value_part in values[::2]:  # перечисляем все куски с шагом 2
            value = '%s%s%s%s' % (value, value_part, key, values[n+1], )
            n += 2
            cycle += 1
            print 'n: ', n, ' cycle: ', cycle
    return value
