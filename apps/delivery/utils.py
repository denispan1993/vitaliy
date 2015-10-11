# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def parsing(value, key, ):
    from re import split
    values = split("{{ id }}*", value, )
    print value.encode('utf8', )
    print values[0].encode('utf8', )
    n = 0
    cycle = 0
    part_count = len(values, )
    print 'part_count: ', part_count
    if part_count > 1:
        value = ''
        for value_part in values[::2]:  # перечисляем все куски с шагом 2
            #if n % 2 == 0:
            value1 = values[cycle]
            value = '%s%s%s' % (value, value1, key, )
            #else:
                #value1 = values[cycle]
                #value = '%s%s%s' % (value, value1, key, )
            print 'value1: ', value1.encode('utf8', )
            print 'value: ', value.encode('utf8', )
            print 'n: ', n, ' cycle: ', cycle
            n += 2
            cycle += 1
        return value
    else:
        return value
