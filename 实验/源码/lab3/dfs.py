import copy
# import time
import os
import psutil
forward=[[0,1],[1,0],[-1,0],[0,-1]] #向右 向下 向上 向左
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
    
def get_front(s): return int(s[:s.find(",")])
def get_behind(s):return int(s[s.find(",")+1:]) 
    
def dfs(x,y,maze,record):
    if maze[x][y]=='E':
        return True
    else:
        for i in range(0,4):
            fx=forward[i][0]
            fy=forward[i][1]
            if judge(x+fx,y+fy,maze)==True and (record[x+fx][y+fy]=='0' or record[x+fx][y+fy]=='E'):
                record[x+fx][y+fy]='1'
                if dfs(x+fx,y+fy,maze,record)==True:
                    his=str(x+fx)+","+str(y+fy)
                    ans.append(his)
                    return True
        return False
    
def replace_maze(maze,history):
    for i in range(0,len(history)):
        maze[get_front(history[i])][get_behind(history[i])]="*"
    return maze

# start=time.time()

file="D:\\code\\python\\homework_needs\\MazeData.txt"
maze=read(file)
row=len(maze)
maze=cut(maze)
col=len(maze[1])
x=y=0
for i in range(1,row):
    for j in range(0,col-1):
        if maze[i][j]=='S':
            x=i
            y=j
            break
record=copy.deepcopy(maze)
dfs(x,y,maze,record)
del ans[:1]
sum=0
maze=replace_maze(maze,ans)
for i in range(0,row):
    for j in range(0,col-1):
        if maze[i][j]=='*':
            sum+=1
            print("\033[7;37;46m"+'0'+"\033[0m",end='')
        else:
            print(maze[i][j],end='')
    print('1')
print("路径总长度为：",sum)

# end=time.time()
# print(end-start)
print(u'当前进程的内存使用：%.4f GB'
% (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )