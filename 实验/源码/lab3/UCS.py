import copy
# import time
import os
import psutil
forward=[[0,1],[1,0],[-1,0],[0,-1]] #向左 向右 向上 向下
que=[]
ans=[]
def read(filename): #读入文件
    content=[]
    with open(filename,'r') as file_object:
        for line in file_object.readlines():
            content.append(line) 
        return content

def cut(maze): #将迷宫切分成一个个小方块，方便后续路径的替换 尾部的换行符要删掉
    for i in range(0,len(maze)):
        maze[i]=list(maze[i])
        maze[i].pop()
    return maze

def judge(a,b,maze): #判断某个方向能否前进
    if maze[a][b]==1: return False
    else: return True

def trans(maze,row,col): #转换 因为把原图中的0换成了距离，因此可能会有与墙相同的数字 所以把墙换成-1
    for i in range(0,row):
        for j in range(0,col):
            if maze[i][j]=='1':
                maze[i][j]='-1'
    return maze

def sort(): #排序 每次选择成本最小的路
    for i in range(0,len(que)-1):
        for j in range(i+1,len(que)):
            if que[j-1][0] > que[j][0]:
                que[j-1],que[j]=que[j],que[j-1]

def find(x,y):
    for i in range(0,len(ans)):
        if ans[i][0]==x and ans[i][1]==y: return i

def add_q(x,y,maze,record,sum):
    flag=0
    for i in range(0,4):
        fx=forward[i][0]
        fy=forward[i][1]
        if record[x+fx][y+fy]=='E':
            for j in range(0,len(que)): 
                que.pop()
            new_add=["ans",x+fx,y+fy,x,y]
            que.append(new_add) #只剩唯一可拓展的
            flag=1
        elif judge(x+fx,y+fy,maze)==True and (record[x+fx][y+fy]=='0'):
            if maze[x][y]=='S': 
                # new_add=[int(maze[x+fx][y+fy]),x+fx,y+fy,x,y] #最后两个x y是扩展点来源
                new_add=[sum,x+fx,y+fy,x,y] #最后两个x y是扩展点来源
            else:
                # new_add=[int(maze[x+fx][y+fy])+int(maze[x][y]),x+fx,y+fy,x,y]
                new_add=[sum,x+fx,y+fy,x,y]
            que.append(new_add)
    if flag==0: sort()

def ucs(x,y,maze,record,):
    ox=oy=0
    sum=0
    while maze[x][y]!='E' and len(que)>0:
        sum+=1
        ans.append([x,y,ox,oy])
        record[x][y]='-1'
        if maze[x][y]!='S':
            add_q(x,y,maze,record,sum)
        ox=que[0][3]
        oy=que[0][4]
        x=que[0][1]
        y=que[0][2]
        del que[0]
    ans.append([x,y,ox,oy])

def replace_map(maze,ans,x,y):
    i=ans[-1][2]
    j=ans[-1][3]
    while i!=x or j!=y:
        p=find(i,j)
        maze[i][j]="*"
        i=ans[p][2]
        j=ans[p][3]
    return maze

# start=time.time()

file="D:\\code\\python\\homework_needs\\MazeData.txt"
maze=read(file)
row=len(maze)
maze=cut(maze)
col=len(maze[1])-1
map=copy.deepcopy(maze)
x=y=ex=ey=0
maze=trans(maze,row,col)
for i in range(1,row):
    for j in range(1,col):
        if maze[i][j]=='S':
            x=i
            y=j
        if maze[i][j]=='E':
            ex=i
            ey=j
record=copy.deepcopy(maze)
add_q(x,y,maze,record,1)
ucs(x,y,maze,record)
map=replace_map(map,ans,x,y)
sum=0
for i in range(0,row):
    for j in range(0,col):
        if map[i][j]=='*':
            sum+=1
            print("\033[7;37;46m"+'0'+"\033[0m",end='')
        else:
            print(map[i][j],end='')
    print('1')
print("路径总长度为：",sum)

# end=time.time()
# print(end-start)
print(u'当前进程的内存使用：%.4f GB'
% (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )