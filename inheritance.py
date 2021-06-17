class Employee:
    # class variable
    raise_amount = 100

    def __init__(self, name, money):
        self.name = name
        self.money = money

    def apply_raise(self):
        self.money += self.raise_amount  # self.xyz, there's a lookup chain

    def __str__(self):
        return f"{self.name} earns {self.money} every year."


class Developer(Employee):
    raise_amount = 200

    def __init__(self, name, money, programing_language):
        # Employee.__init__(self, name, money)
        # allowed when you use multiple inheritance
        super().__init__(name, money)
        self.programing_language = programing_language


shun = Employee("shun", 10000)
shun.apply_raise()
charlie = Developer("charlie", 20000, "python")
charlie.apply_raise()
print(shun)
print(charlie)
