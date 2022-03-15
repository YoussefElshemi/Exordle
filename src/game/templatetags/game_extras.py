from django import template

register = template.Library()

# check if index is in an array
def exists(arr, idx):
    return idx - 1 < len(arr)

# return element at index
def get(arr, idx):     
    return str(arr[idx - 1])

def get_css(arr, idx):
    return arr[idx - 1]

register.filter('get', get)
register.filter('exists', exists)
register.filter('get_css', get_css)