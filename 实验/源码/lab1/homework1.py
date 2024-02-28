def find_key(key,letter):
    for k in letter.keys():
        if k==key:
            return True
    return False

list=input().split()
m=int(list[0]) #节点数
n=int(list[1]) #边数
arr=[]

for i in range(0,m):
    arr.append([])
    for j in range(0,m):
        if i==j:
            arr[i].append(0)
        else:
            arr[i].append(99)

letter={}
sign=0
for i in range(0,n):
    list1=input().split()
    u=list1[0]
    v=list1[1]
    #想办法将uv代表的字母转换成数字
    if find_key(u,letter)==False:
        letter[u]=sign
        sign+=1
    if find_key(v,letter)==False:
        letter[v]=sign
        sign+=1
    value=int(list1[2])
    arr[letter[u]][letter[v]]=value
    arr[letter[v]][letter[u]]=value

list=input().split()
begin=letter[list[0]] #要访问的结点
end=letter[list[1]]

low=arr[begin][:]
visit=[value*0 for value in range(0,m)]
visit[begin]=1
min=99
k=0
for i in range(0,m):
    min=99
    for j in range(0,m):
        if visit[j]==0 and low[j]<min:
            min=low[j]
            k=j
    visit[k]=1
    for j in range(0,m):
        if low[k]+arr[k][j]<low[j]:
            low[j]=low[k]+arr[k][j]
    if k==end:
        break

print(low[end])