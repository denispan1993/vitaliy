# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def parsing(value, key, ):
    from re import split
    values = split("{{ id }}*", value, )
    cycle = 0
    part_count = len(values, )
    if part_count > 1:
        value = ''
        for value_part in values:  # [::2]:  # перечисляем все куски с шагом 2
            value = '%s%s%s-%d-%d' % (value, value_part, key, part_count, cycle, )
            cycle += 1
            if part_count == cycle:
                break
    return value
