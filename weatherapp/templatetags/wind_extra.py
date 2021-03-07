from django import template

register = template.Library()


@register.simple_tag(name="dir")
def wind_direction(degree):
    wind_dirs = {0: "N",
                 45: "NE",
                 90: "E",
                 135: "SE",
                 180: "S",
                 225: "SW",
                 270: "W",
                 315: "NW",
                 360: "N"}

    degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    return wind_dirs[min(degrees, key=lambda x:abs(x-degree))]
