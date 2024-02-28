import matplotlib.pyplot as plt
def f(x,y):
    return 4*x*x-4*x*y+2*y*y

def dfx(x,y):
    return 8*x-4*y

def dfy(x,y):
    return 4*y-4*x

learn_rate=0.15
min=0.000000001
x,y=2,3
J=f(x,y)
count=0 #记录迭代次数
x_ray=[]
y_ray=[]
while True:
    count+=1
    last_J=J
    last_x,last_y=x,y
    x=x-learn_rate*dfx(last_x,last_y)
    y=y-learn_rate*dfy(last_x,last_y)
    J=f(x,y)
    loss=abs(J-last_J)
    x_ray.append(count)
    y_ray.append(loss)
    if(loss<min or count>=1000): 
        break
print("x:","%.6f"%x, "y:","%.6f"%y)
print("学习率为:",learn_rate, "迭代次数为:",count)
plt.plot(x_ray, y_ray)
plt.show()