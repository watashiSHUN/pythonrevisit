# NOTE: how rect update all attributes with one function
class ShunRect:
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom

    # intercept attribute assignment
    def __setattr__(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = value  # constructor init
        elif key == "top":
            diff = value - self.__dict__["top"]
            self.__dict__[key] = value
            # assume there's bottom already
            self.__dict__["bottom"] = self.__dict__["bottom"] + diff
            # NOTE to avoid recursion self.top = value


shunrect = ShunRect(100, 50)
shunrect.top = 1000
print(shunrect.bottom)
