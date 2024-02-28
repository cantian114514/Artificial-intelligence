import copy
import time
import os
import psutil
goal=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
next=[[-1,0],[1,0],[0,-1],[0,1]]
close=set()
history=0

#14 10 6 0 4 9 1 8 2 3 5 11 12 13 7 15
# 6 10 3 15 14 8 7 11 5 1 0 2 13 12 9 4
# 5 1 3 4 2 7 8 12 9 6 11 15 0 13 10 14
# 1 2 4 8 5 7 11 10 13 15 0 3 14 6 9 12

def man_dist(arr):  #计算曼哈顿距离
    ans=0
    for i in range(0,16):
        if arr[i]!=0 and arr[i]!=goal[i]:
            x=int((arr[i]-1)/4)
            y=arr[i]-4*x-1
            ans+=abs(x-int(i/4))+abs(y-(i%4))
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
    return linear_conflict(arr)

def children(arr_):
    index=0
    for i in range(0,16):
        if arr_[i]==0:
            index=i  #找到0的坐标
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
            ans.append(arr)
    return sorted(ans,key=lambda x:h(x))

def dfs(way,g,bound):
    global history
    node=way[-1]
    f=g+h(node)
    history+=1
    if f>bound: 
        return f
    if node==goal: 
        return -1 #找到目标
    
    min=6666
    for i in children(node):
        k=tuple(i)
        if k in close: continue
        way.append(i)
        close.add(k) #路经检测

        t=dfs(way,g+1,bound)
        if t==-1:
            return -1
        if t<min:
            min=t
        way.pop()
        close.remove(k)
    return min

def IDA(start):
    bound=h(start)
    way=[start]  #更新的路径合集
    close.add(tuple(start))
    while(1):
        t=dfs(way,0,bound)
        if t==-1:
            return way
        if t>60:
            return None
        bound=t #更新bound

def print_ans(ans):
    ans_list=[]
    for k in range(1,len(ans)):
        index=0
        for i in range(0,16):
                if ans[k-1][i]==0:
                    index=i
                    break
        ans_list.append(ans[k][index])
    print("每次移动的数字块：",ans_list)
        
#数据读入
temp=input().split()
start=time.time()
arr=[]
sum=0
for i in range(0,16):
    arr.append(int(temp[sum]))
    sum+=1

ans=IDA(arr)
print_ans(ans)
print("访问过的节点数",history)

end=time.time()
print("运行总时间",end-start)
print(u'当前进程的内存使用：%.4f GB'
% (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )