from django import template


register = template.Library()


@register.filter(name='setclass_rm_autocomplete')
def setclass_rm_autocomplete(field, class_input):
    return field.as_widget(attrs={'class': class_input, 'autocomplete': 'off'})
