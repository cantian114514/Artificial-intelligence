#模拟退火
import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

T=10000 #初温
T_end=0.1 #终温
a=0.99 #温度衰减系数
L=500 #循环次数
data=[]
x=[]
y=[]

def read(file):
    ans=[]
    with open(file,'r') as file_object:
        for line in file_object.readlines():
            temp=line.strip()
            temp=temp.split()
            t=[int(temp[0]),float(temp[1]),float(temp[2])]
            x.append(float(temp[1]))
            y.append(float(temp[2]))
            ans.append(t)
    return ans

def get_dist(way): #计算距离总和 算评估函数
    ans=0
    for i in range(1,len(way)+1):
        if i==len(way):
            way1=way[0]-1
            way2=way[len(way)-1]-1
        else:
            way1=way[i-1]-1
            way2=way[i]-1
        x1=data[way1][1]
        y1=data[way1][2]
        x2=data[way2][1]
        y2=data[way2][2]
        ans+=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    return ans

def n1(way):
    p=random.random()
    a,b,c=random.sample(range(1, len(way)-1), 3)
    point=sorted([a,b,c]) #升序
    a,b,c=point[0],point[1],point[2]
    if p<0.5: #交换中间两段
        ans=way[0:a]+way[b:c]+way[a:b]+way[c:len(way)]
    else: #交换首尾两段
        ans=way[c:len(way)]+way[a:b]+way[b:c]+way[0:a]
    return ans

def n2(way):
    i=random.randint(0,len(way)-2)
    j=random.randint(1,len(way)-1)
    while True:
        if i!=j: #如果不相同 则交换两个城市
            way[i],way[j]=way[j],way[i]
            ans=way[:]
            way[i],way[j]=way[j],way[i]
            break
        else:
            i=random.randint(0,len(way)-2)
            j=random.randint(1,len(way)-1)
    return ans

def n3(way):
    a,b=random.sample(range(1, len(way)-1), 2)
    if a>b: a,b=b,a 
    ans=way[0:a]+way[a:b][::-1]+way[b:len(way)] #中间反转
    return ans

def get_neighbur(way): #邻域解
    p=random.random()
    if p<0.5:#分成四段
        a,b,c=random.sample(range(1, len(way)-1), 3)
        point=sorted([a,b,c]) #升序
        a,b,c=point[0],point[1],point[2]
        if p<0.25: #交换中间两段
            ans=way[0:a]+way[b:c]+way[a:b]+way[c:len(way)]
        else: #交换首尾两段
            ans=way[c:len(way)]+way[a:b]+way[b:c]+way[0:a]

    elif p<0.75: #选择其中两个点
        i=random.randint(0,len(way)-2)
        j=random.randint(1,len(way)-1)
        while True:
            if i!=j: #如果不相同 则交换两个城市
                way[i],way[j]=way[j],way[i]
                ans=way[:]
                way[i],way[j]=way[j],way[i]
                break
            else:
                i=random.randint(0,len(way)-2)
                j=random.randint(1,len(way)-1)

    else:#分成三段
        a,b=random.sample(range(1, len(way)-1), 2)
        if a>b: a,b=b,a 
        ans=way[0:a]+way[a:b][::-1]+way[b:len(way)] #中间反转
    return ans

if __name__ == '__main__':
    file="D:\\code\\python\\file\\lab6\\TSP.txt"
    data=read(file)#每一行数据写入到list中

    way=[i for i in range(1,len(data)+1)] #旅行商走过的路径
    random.shuffle(way)   #生成初始随机排列
    distance=get_dist(way)

    record_weight=[] #保存每次最优的距离 呈现变换
    fig1=plt.figure(1)
    gif_pic=[] #保存动态图

    #生成初始状态
    new_way=[]
    new_dist=0
    best_way=way
    best_dist=distance
    s=0

    while True:
        s+=1
        #满足终止条件：连续两次的更新值一致 说明已经到最好状态
        if T<=T_end:
            break
        for i in range(L): #邻域中选解 找最好的一个
            # new_way=n1(way)
            # new_way=n2(way)
            # new_way=n3(way)
            new_way=get_neighbur(way)
            new_dist=get_dist(new_way)
            minus=new_dist-distance
            if new_dist<distance: #新产生的节点比当前更好 接受
                way=new_way
                distance=new_dist
                record_weight.append(distance)
            else: #未优于 根据概率选取
                p=math.exp(-minus/T) #当前状态的概率值
                q=random.random() #生成0~1的随机数
                if p>q:
                    way=new_way
                    distance=new_dist
            if distance<best_dist:
                best_way=way
                best_dist=distance #更新最优解
        T=T*a

        if s%10==0:
            x=[]
            y=[]
            for i in way:
                x.append(data[i-1][1])
                y.append(data[i-1][2])
            x.append(data[0][1])
            y.append(data[0][2]) 
            plt.title('process')
            pic=plt.plot(x, y, marker = '.', color = 'blue',linewidth=1) 
            gif_pic.append(pic)

    print(best_way)
    print(best_dist)

    #GIF保存
    ani=animation.ArtistAnimation(fig1,gif_pic,interval=200, repeat_delay=1000)
    ani.save("SA_TSP.gif",writer='pillow')

    fig2=plt.figure(2) #展现最优距离的变化
    plt.title('cost change')
    x_=[i for i in range(len(record_weight))] #横轴
    plt.plot(x_,record_weight) #横轴纵轴
    plt.show()