import module

def read(filename):
    content=[]
    try:
        with open(filename,'r') as file_object:
            for line in file_object.readlines():
                content.append(line.lower()) #全部以小写状态读入
    except FileNotFoundError:
        print("Sorry,the file",filename," does not exist.")
    else:
        return content
        
file='D:\\code\\python\\homework_needs\\Romania.txt'
content=read(file)
arr=[]
low=[]
num_to_city={}
letter={}
module.create_map(content,arr,low,num_to_city,letter)
list=input().split()
begin=letter[list[0][0].lower()]
end=letter[list[1][0].lower()] #转小写
for i in range(0,len(low)):
    low[i].distant=arr[begin][i]
    low[i].way=num_to_city[begin]

list=content[0].split()
m=int(list[0]) #节点数

visit=[value*0 for value in range(0,m)]
visit[begin]=1
min=1000
k=0
for i in range(0,m):
    min=1000
    for j in range(0,m):
        if visit[j]==0 and low[j].distant<min:
            min=low[j].distant
            k=j
    visit[k]=1
    for j in range(0,m):
        if low[k].distant+arr[k][j]<low[j].distant:
            low[j].distant=low[k].distant+arr[k][j]
            low[j].way=low[k].way+" → "+num_to_city[k]
    if k==end:
        break
low[end].way=low[end].way+" → "+num_to_city[end]
print(low[end].way.title(),low[end].distant)

diary='D:\\code\\python\\homework_needs\\diary.txt'

with open(diary,'w') as file_object:
    file_object.write("the way and the least distant:\n")
    file_object.write(low[end].way.title())
    file_object.write("\n")
    file_object.write(str(low[end].distant))
    file_object.write("\n")