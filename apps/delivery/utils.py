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
            if part_count == cycle:
                break
            value = '%s%s%s' % (value, value_part, key, )
            cycle += 1
    return value
