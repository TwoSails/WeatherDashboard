from django import template

register = template.Library()


@register.simple_tag(name='round')
def roundValue(value, arg, key=None):
    if type(value) == type(float(arg)):
        return round(value, arg)
    elif type(value) == type({}) and key == "speed":
        point = 0
        for x in (value[key]):
            point += x
        return round(point / len(value[key]), arg)
    elif type(value) == type({}) and key == "gust":
        return round(max(value[key]), arg)
    elif key == "rainfall":
        rainfall = 0
        for x in value:
            rainfall += x
        return round(rainfall, 1)
    else:
        print(value, key, arg, type(value))
        return 0.0
