import copy
import time
import heapq
import os
import psutil
goal=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
next=[[0,1],[0,-1],[1,0],[-1,0]]
close=set()
flag=-1

class node():
    def __init__(self,f,arr,path,g):
        self.f=f
        self.arr=arr
        self.path=path
        self.g=g
    def __lt__(self, node): # heapq的比较函数
        if self.f == node.f:
            return self.g > node.g
        return self.f < node.f

def man_dist(arr):  #计算曼哈顿距离
    ans=0
    for i in range(0,16):
        if arr[i]!=0 and arr[i]!=goal[i]:
            x=(arr[i]-1)//4
            y=arr[i]-4*x-1
            ans+=abs(x-(i//4))+abs(y-(i%4))
    return ans

def wrong_card(arr):
    ans=0
    for i in range(0,16):
        if arr[i]!=0 and arr[i]!=goal[i]:
            ans+=1
    return ans

def linear_conflict(arr):
    board=[arr[0:4],arr[4:8],arr[8:12],arr[12:16]]
    n = len(board)
    linear_conflicts = 0
    # 计算每一行的线性冲突
    for i in range(n):
        for j in range(n):
            tile1 = board[i][j]
            if tile1 == 0:
                continue
            goal_row1, goal_col1 = (tile1 - 1) // n, (tile1 - 1) % n
            if goal_row1 == i:  # 需要在同一行内进一步检查
                for k in range(j + 1, n):
                    tile2 = board[i][k]
                    if tile2 == 0:
                        continue
                    goal_row2, goal_col2 = (tile2 - 1) // n, (tile2 - 1) % n
                    if goal_row2 == i and goal_col2 < goal_col1:
                        linear_conflicts += 1
    # 计算每一列的线性冲突
    for j in range(n):
        for i in range(n):
            tile1 = board[i][j]
            if tile1 == 0:
                continue
            goal_row1, goal_col1 = (tile1 - 1) // n, (tile1 - 1) % n
            if goal_col1 == j:  # 需要在同一列内进一步检查
                for k in range(i + 1, n):
                    tile2 = board[k][j]
                    if tile2 == 0:
                        continue
                    goal_row2, goal_col2 = (tile2 - 1) // n, (tile2 - 1) % n
                    if goal_col2 == j and goal_row2 < goal_row1:
                        linear_conflicts += 1
    return man_dist(arr) + linear_conflicts

def h(arr):  #h(n) 应用不同的启发函数时就改变这里
    # return man_dist(arr)
    # return wrong_card(arr)
    return linear_conflict(arr)
# -----------------------------------------------------------

def move(arr_,path,history): #生成子节点
    for i in range(0,16): #找到0的坐标
        if arr_[i]==0:
            index=i
            break
    ans=[]
    x=index//4
    y=index%4
    for i in range(0,4):
        fx=next[i][0]
        fy=next[i][1]
        new_index=index+fx*4+fy
        if x+fx>-1 and x+fx<4 and y+fy>-1 and y+fy<4:
            arr=copy.deepcopy(arr_)
            arr[index]=arr[new_index]
            arr[new_index]=0
            ans.append([arr,str(arr[index])])
            if arr==goal:
                global flag
                flag=1
                print("走过的路径",path+str(arr[index])+" ")
                print("访问的总结点数",history)
    return ans

def A_star(start): #遍历用
    n1=node(h(start),start,"",0)
    open=[n1]
    heapq.heapify(open)  #用堆来记录，省时
    history=0
    while len(open)!=0:
        top=heapq.heappop(open)
        history+=1
        if flag!=-1:
            break
        for i in move(top.arr,top.path,history):
            if tuple(i[0]) in close:continue
            close.add(tuple(i[0]))
            child=node(top.g+h(i[0]),i[0],str(top.path+i[1]+" "),top.g+1)
            heapq.heappush(open,child)
    if len(open)==0: print("no solution")

#数据读入
temp=input().split()
arr=[]
start=time.time()
sum=0
for i in range(0,16):
    arr.append(int(temp[sum]))
    sum+=1
A_star(arr)

end=time.time()
print("运行的总时间",end-start)
print(u'当前进程的内存使用：%.4f GB'
% (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )