"""
ООП затестил ток здесь потому что я пока совсем в него не умею, а над фласком долго пыхтеть не хочу) 
"""


class Down:
    entity = "Retarded guy"
    strength = 2

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    def be_down(self):
        print(f"Hi, Im down. My name is {self.age} and im {self.name} years old!")


gus = Down("Gus", 14)


class CompleteIdiot(Down):
    strength = 4

    def say_my_name(self):
        print("U are god damn right!")

waltuth = CompleteIdiot("Walter White", 45)


class InsaneManiac:
    entity = "Psycho"
    strength = 10

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    def be_psycho(self):
        print(f"I am {self.name} and ima kill u!")

patric = InsaneManiac("Patric Bateman", 25)

class LiterallyMe(InsaneManiac, Down):
    def say_it(self):
        print("Wow, thats literrally me!")

me = LiterallyMe("ALex", 20)

print(gus.entity)
print(gus.strength)
gus.be_down()

print(waltuth.entity)
print(waltuth.strength)
waltuth.be_down

print(patric.entity)
print(patric.strength)
patric.be_psycho()

print(me.entity)
print(me.strength)
me.be_down()
me.be_psycho()
me.say_it()

gus.entity = "Gustavo"

print(Down.entity)
print(gus.entity)
print(waltuth.entity)