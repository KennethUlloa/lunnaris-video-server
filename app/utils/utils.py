from random import randint
from flask import request

def genToken(n):
    result           = ''
    characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range(0, n):
        index = randint(0, charactersLength-1)
        result += characters[index]
    return result

def require_auth(callback, *c_args, **c_kwargs):
    def wrap_function(func):
        def exe_func(*args, **kwars):
            authenticated, response = callback(*c_args, **c_kwargs)
            if not authenticated:
                return response
            return func(*args, **kwars)
        exe_func.__name__ = func.__name__
        return exe_func
    return wrap_function

def handle_null(value, default) -> object:
    if value == None: 
        return default
