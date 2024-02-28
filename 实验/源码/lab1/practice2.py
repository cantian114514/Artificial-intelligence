# #homework9
# magicians=['doudz','ahrenl','cantian']

# def show_magicians(magicians):
#     print("Magicians:")
#     for i in range(len(magicians)):
#         print("-",magicians[i])

# def make_great(magicians):
#     for i in range(len(magicians)):
#         magicians[i]="the Great "+magicians[i]
#     show_magicians(magicians)

# show_magicians(magicians[:])
# make_great(magicians)

#homework10
class Restaurant():
    def __init__(self,restaurant_name,cuisine_type):
        self.restaurant_name=restaurant_name
        self.cuisine_type=cuisine_type
        self.number_served=0

    def describe_restaurant(self):
        print("Restaurant's information:")
        print("Name:",self.restaurant_name)
        print("Cuisine type:",self.cuisine_type)

    def open_restaurant():
        print("The restaurant is opening")

    def set_number_served(self,num):
        self.number_served=num
    
    def increment_number_served(self,num):
        self.number_served+=num

my_restaurant=Restaurant('萨莉亚','意大利面')
print(my_restaurant.number_served)
my_restaurant.number_served=114514
print(my_restaurant.number_served)
my_restaurant.set_number_served(1919)
print(my_restaurant.number_served)
my_restaurant.increment_number_served(810)
print(my_restaurant.number_served)

# class IceCreamStand(Restaurant):
#     def __init__(self, restaurant_name, cuisine_type,flavors):
#         super().__init__(restaurant_name, cuisine_type)
#         self.flavors=flavors

#     def describe_restaurant(self):
#         print("IceCreamStand:")
#         super().describe_restaurant()
#         print("flavors:",self.flavors)
    
# my_icecreamstand=IceCreamStand('麦当劳','麦旋风','奥利奥风味')
# my_icecreamstand.describe_restaurant()

#homework11
# def analysis(filename):
#     try:
#         with open(filename,'r') as file_object:
#             contents=file_object.read()
#     except FileNotFoundError:
#         print("Sorry,the file",filename," does not exist.")
#     else:
#         length=len(contents.split())
#         print("There are",length,"words in total")
#         num_the=contents.lower().count('the')
#         print("There are",num_the,"'the' words in total")

# file='D:\\code\\python\\homework_needs\\bible.txt'
# analysis(file)

# #homework12
# game={"hollow_knight":"Team Cherry",
#       "the_binding_of_issac":"Edmund McMillen,Florian Himsl",
#       "elden_ring":"Miyazaki Hidetaka"}
# try:
#     search=game["silksong"]
# except KeyError:
#     print("this game does not exist!")
# else:
#     print("The producer of this game:",search)