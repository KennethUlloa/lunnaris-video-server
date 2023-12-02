class Tester:
    tests = []
    def test(self, *args, expected = None):
        def decorator(func):
            test_arc = {
                'func': func,
                'args': args,
                'expected': expected
            }
            self.tests.append(test_arc)
            return func
        return decorator
    
    def run(self):
        for i, f in enumerate(self.tests):
            func = f['func']
            args = f['args']
            expected = f['expected']
            if func(*args) == expected:
                print(f'Test {i}: {func.__name__} passed')
            else:
                print(f'Test {i}: {func.__name__} failed')



