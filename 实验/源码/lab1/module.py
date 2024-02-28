class city():
    def __init__(self,way,distant):
        self.way=way
        self.distant=distant

def find_key(key,letter):
    for k in letter.keys():
        if k==key:
            return True
    return False

def create_map(content,arr,low,num_to_city,letter):
    list=content[0].split()
    m=int(list[0]) #节点数
    n=int(list[1]) #边数

    for i in range(0,m):
        arr.append([])
        for j in range(0,m):
            if i==j:
                arr[i].append(0)
            else:
                arr[i].append(1000) #数组初始化

    sign=0
    i=0
    for i in range(1,n+1):
        list1=content[i].split()
        u=list1[0][0]
        v=list1[1][0] #开头首字母
        #想办法将uv代表的字母转换成数字
        if find_key(u,letter)==False:
            letter[u]=sign
            num_to_city[sign]=list1[0]
            sign+=1
            mycity1=city(list1[0],0)
            low.append(mycity1)
        if find_key(v,letter)==False:
            letter[v]=sign
            num_to_city[sign]=list1[1]
            sign+=1
            mycity2=city(list1[1],0)
            low.append(mycity2)
        value=int(list1[2])
        arr[letter[u]][letter[v]]=value
        arr[letter[v]][letter[u]]=value
        #建图完成