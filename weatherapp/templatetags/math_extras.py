from django import template

register = template.Library()


@register.simple_tag(name='round')
def roundValue(value, arg, key=None):
    if isinstance(value, float):
        return round(value, arg)
    elif isinstance(value, dict) and key == "speed":
        point = 0
        for x in (value[key]):
            point += x
        return round(point / len(value[key]), arg)
    elif isinstance(value, dict) and key == "gust":
        return round(max(value[key]), arg)
    elif key == "rainfall":
        rainfall = 0
        for x in value:
            rainfall += x
        return round(rainfall, 1)
    else:
        print('roundValue func', value, key, arg, type(value))
        return 0.0
