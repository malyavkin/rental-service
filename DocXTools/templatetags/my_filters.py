from django import template

register = template.Library()


@register.filter(name='times')
def times(number, step=1):
    return range(0, number, step)


@register.filter(name='eq')
def eq(eql, eqr):
    print('comparing {} to {} ({})'.format(eql, eqr, eql == eqr) )
    return eql == eqr


@register.filter(name='typ')
def typ(val):
    print('{{{}}} {}'.format(type(val), val) )
    return '{{{}}} {}'.format(type(val), val)
