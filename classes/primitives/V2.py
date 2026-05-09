

# define a type Vector 2.
class V2(list[int|float]):

    def __init__(self, *elements: list[int|float]):
        if len(elements) != 2:
            raise Exception('V2 allow only two values.')
        self.append(elements[0])
        self.append(elements[1])

    # getter.
    @property
    def x(self) -> int|float:
        return self[0]
    @x.setter
    def x(self, value: int|float):
        self[0] = value
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value: int|float):
        self[1] = value

    # cast dictionary.
    def __iter__(self):
        yield self[0]
        yield self[1]
    
    # cast dictionary.
    def __dict__(self):
        return { 'x': self.x, 'y': self.y }

        