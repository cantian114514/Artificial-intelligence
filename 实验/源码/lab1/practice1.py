# #homework1
# message1="Hello World"
# print(message1)
# print("\n")

# #homework2
# message2=input("please enter a message\n")
# print(message2)
# print("\n")

# #homework3
# add=5+3
# sub=10-2
# mul=2*4
# div=round(24/3)
# print(add,sub,mul,div)
# print("\n")

# #homework4
# famous_person="Nietzsche"
# message3="\"To be is to do\""
# print(famous_person,"once said,",message3)
# print("\n")

# #homework5
# s="\n\tSchool of Computer Science and Engineering\n"
# print(s.lstrip())
# print(s.rstrip())
# print(s.strip())
# ss=s.strip()
# print(ss.title())
# print(ss.lower())
# print(ss.upper())
# print("\n")

# #homework6
# alien_color=input("green yellow red please enter one of them\n")
# if alien_color=="green":
#     print("now you get 5 points")
# elif alien_color=="yellow":
#     print("now you get 10 points")
# elif alien_color=="red":
#     print("now you get 15 points")
# else:
#     print("dont have this color")

# #homework7
# s=0
# for even in range(0,101,2):
#     s+=even
# print(s)

# #homework8
# import random
# num=random.randint(0,100)
# a=input("please enter a num in 0~100\n")
# sum=1
# while num!=int(a):
#     if num>int(a):
#         a=input("the true number is bigger,try again!\n")
#         sum+=1
#     elif num<int(a):
#         a=input("the true number is smaller,try again!\n")
#         sum+=1
# print("you are right!you have tried",sum,"times!\n")

# #homework7
# print(sum(list(range(1,101,1))))

# #homework8
# r1=int(input("please enter r1's row\n"))
# both=int(input("please enter r1's column and r2's row\n"))
# c2=int(input("please enter r2's column\n"))
# R1=[]
# R2=[]
# res=[]
# for i in range(r1):
#     ri1=input().split()
#     R1.append([int(i) for i in ri1])
# for i in range(both):
#     ri2=input().split()
#     R2.append([int(i) for i in ri2])

# for i in range(r1):
#     res.append([])
#     for j in range(c2):
#         sum = 0
#         for k in range(both):
#             sum+=R1[i][k]*R2[k][j]
#         res[i].append(sum)

# for i in range(r1):
#     print(res[i])

# #homework9
# #three cities with their country population fact information in didictionary
# beijing={"country":"China",
#          "population":"21893095",
#          "fact":"Beijing is the capital of China."}

# Denver={"country":"America",
#         "population":"693060",
#         "fact":"Denver is the biggest city in Colorado."}

# Jerusalem={"country":"Israel and Palestine",
#            "population":617042,
#            "fact":"Jerusalem is the Holy land of Christianity,Judaism ans islam."}

# cities={"Beijing":beijing,"Denver":Denver,"Jerusalem":Jerusalem}
# for name,city in cities.items():
#     print(name,"'s information:",city)