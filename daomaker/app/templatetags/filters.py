from django.template.defaultfilters import register


@register.filter(name='truncate')
def truncate(string, length):
    try:
        if len(string) > int(length):
            return string[:int(length)] + "..."
        return string
    except TypeError:
        return "-"
