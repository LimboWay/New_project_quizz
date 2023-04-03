from django import template

register = template.Library()


# filter
def negative(value):        # -5
    return -value


# filter
def multi(value, arg):
    return value * arg


# filter
def dived(value, arg):
    return value // arg


def points(v1, v2):
    if (point := v1 - v2) > 0:
        return point
    return 0


register.filter('negative', negative)
register.filter('multi', multi)
register.filter('dived', dived)
register.filter('points', points)
