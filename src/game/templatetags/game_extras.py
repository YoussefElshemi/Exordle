from django import template

register = template.Library()

def exists(arr, idx):
    return idx - 1 < len(arr)

def get(arr, idx):
    return str(arr[idx - 1])

register.filter('get', get)
register.filter('exists', exists)