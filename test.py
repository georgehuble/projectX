class Foo:
    def __getitem__(self, item):
        return item

f = Foo()
print(next(iter(f)))
