from django import template


register = template.Library()


@register.filter(name='setclass')
def setclass(field, class_input):
    return field.as_widget(attrs={'class': class_input})
