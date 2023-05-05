def argumented_wrapper(path):
    print("i'm a path" + path)
    def wrapper_func(func):
        def wrapped_func(*args, **kwargs):
            print("wrapp_function")
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_func

@argumented_wrapper('aaaaa')
def say_hello(greet):
    print("hello " + greet)

if __name__ == "__main__":
    say_hello("Kenneth")
