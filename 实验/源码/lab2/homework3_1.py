import time
dic={0:'a',1:'b',2:'c',3:'d',4:'e'}

def cutspace(ss):
    n=len(ss)
    i=2
    while i<n:
        if ss[i]==" " and ss[i-2]!=")":
            # ss=ss.replace(ss[i],"")
            list1=list(ss)
            list1.pop(i)
            ss=''.join(list1)
            n-=1
        i+=1
    return ss
def cutsign(l):
    for i in range(0,len(l)):
        if l[i][-1]==',':
            ss=l[i][0:-1]
            l[i]=ss
    return l

def opposite(a): #取反
    ans1=""
    if a[0]!="¬":
        ans1="¬"+a
    else:
        ans1=a[1:len(a)]
    return ans1

def cuthead(a): #取谓词
    ans1=a[0:a.find("(")]
    return ans1

def get_one_case(eg): #取单例
    return eg[eg.find("(")+1:eg.find(")")]

def get_front_case(eg): #取双例的前部分
    return eg[eg.find("(")+1:eg.find(",")]

def get_behind_case(eg): #取单例的后部分
    return eg[eg.find(",")+1:eg.find(")")]

def isvar(f): #判断是否是变量
    if f in['x','y','z','u','v','w']: return True
    else: return False
    
def countvar(case): #统计变量数
    sum=0
    for i in range(0,len(case)):
        if isvar(case[i])==True:
            sum+=1
    return sum

def judgecase(case1,case2):
    ans="none"
    if isvar(case1[0]):
        if case1[1]!=case2[1]: return ""
        else: 
            ans="("+case1[0]+"="+case2[0]+")"
            return ans
    elif isvar(case2[0]):
        if case1[1]!=case2[1]: return ""
        else:
            ans=ans="("+case2[0]+"="+case1[0]+")"
            return ans
    elif isvar(case1[1]):
        if case1[0]!=case2[0]: return ""
        else:
            ans=ans="("+case1[1]+"="+case2[1]+")"
            return ans
    elif isvar(case2[1]):
        if case1[0]!=case2[0]: return ""
        else:
            ans=ans="("+case2[1]+"="+case1[1]+")"
            return ans
    elif case1[0]==case2[0] and case1[1]==case2[1]:
        return ans
    else: return ""

def judge(list1,list2): #判断这两个结点有无可合一的部分
    list1_index=-1
    list2_index=-1
    flag1=0
    for i in range(0,len(list1[0])):
        head1=cuthead(list1[0][i])
        for j in range(0,len(list2[0])):
            head2=cuthead(list2[0][j])
            if head1==opposite(head2):
                list1_index=i
                list2_index=j
                flag1=1
                break
        if flag1==1:
            break
    if list1_index==-1 and list2_index==-1: return []
    else: #谓词可合一
        f1=str(list1[0][list1_index])
        f2=str(list2[0][list2_index])
        length=f1.count(",")
        if length==0:
            case1=get_one_case(f1)
            case2=get_one_case(f2)
            if case1==case2:
                return [list1_index,list2_index,"none"]
            elif isvar(case1)==True and isvar(case2)==False:
                return [list1_index,list2_index,"("+case1+"="+case2+")"]
            elif isvar(case1)==False and isvar(case2)==True:
                return [list1_index,list2_index,"("+case2+"="+case1+")"]
            else:
                return []
        elif length==1:
            case1=[get_front_case(f1),get_behind_case(f1)]
            if countvar(case1)>1: return []
            case2=[get_front_case(f2),get_behind_case(f2)]
            if countvar(case2)>1: return []
            ss=judgecase(case1,case2)
            if ss=="":return []
            else: return[list1_index,list2_index,ss]       

def unify(list1,list2,i,j,l): #合一
    re=judge(list1,list2)
    if len(re)==0:
        return l
    l.append([])
    tail1=dic[re[0]]
    tail2=dic[re[1]]
    if len(list1[0])>1: a=str(i)+str(tail1)
    else: a=str(i)
    if len(list2[0])>1: b=str(j)+str(tail2)
    else: b=str(j)
    ss=re[2]
    t=[]
    l1=list1[0][:]
    l2=list2[0][:]
    for m in range(0,len(l1)):
        l1[m]=l1[m].replace(ss[1],ss[3:len(ss)-1])
    for m in range(0,len(l2)):
        l2[m]=l2[m].replace(ss[1],ss[3:len(ss)-1])
    list1[0]=l1
    list2[0]=l2
    for n in range(0,len(list1[0])):
        if n!=re[0]:
            t.append(list1[0][n])
    for n in range(0,len(list2[0])):
        if n!=re[1] and t.count(list2[0][n])==0:
            t.append(list2[0][n])
    l[len(l)-1].append(t)
    l[len(l)-1].append(a)
    l[len(l)-1].append(b)
    l[len(l)-1].append(ss)
    return l

def getnum(ss):
    if ss[-1]<="z" and ss[-1]>="a": 
        ans=ss[0:-1]
    else: ans=ss
    return ans

def gets(ss,num):
    if ss[-1]<="z" and ss[-1]>="a":
        ans=str(int(num)+1)+ss[-1]
    else:ans=str(int(num)+1)
    return ans
    
def prepareans(l,node,ans,n):
    front=getnum(node[1])
    behind=getnum(node[2])
    if int(front)==-1 or int(behind)==-1:
        return
    tail=""
    if node[len(node)-1]=="none":
        tail=""
    else:
        tail=node[3]
    f=front
    front=gets(node[1],f)
    be=behind
    behind=gets(node[2],be)
    # t=str("R["+str(front)+","+str(behind)+"]"+tail+" = "+str(node[0]))
    t=[str(front),str(behind),tail,str(node[0])]
    ans.append(t)
    if int(f)>=n:prepareans(l,l[int(f)],ans,n)
    if int(be)>=n:prepareans(l,l[int(be)],ans,n)

def correctrow(l,ans,s):
    n=len(s)
    for i in range(0,len(ans)):
        s.append(ans[i]) #完整集 但行数有错误
    for i in range(len(s)-1,n-1,-1):
        s1=int(getnum(s[i][0]))-1
        s2=int(getnum(s[i][1]))-1
        if s1>=n:
            ss1=str(l[s1][0])
            for j in range(n,len(s)):
                if ss1==s[j][3]:
                    s[i][0]=s[i][0].replace(getnum(s[i][0]),str(j+1))
                    break
        if s2>=n:
            ss2=str(l[s2][0])
            for j in range(n,len(s)):
                if ss2==s[j][3]:
                    s[i][1]=s[i][1].replace(getnum(s[i][1]),str(j+1))
                    break
    for i in range(0,len(ans)):
        ans[i]=s[i+n] 

def printans(ans):
    for i in range(0,len(ans)):
        t=str("R["+str(ans[i][0])+","+str(ans[i][1])+"]"+ans[i][2]+" = "+str(ans[i][3]))
        print(t)

def resolution(list_,s):
    flag=0
    sum=0
    while True:
        l=len(list_)
        for i in range(0,l):
            if sum==0:
                j=i+1
            else:
                j=l1
            for j in range(j,l):
                list1=list_[i]
                list2=list_[j]
                list_=unify(list1[:],list2[:],i,j,list_)
                if len(list_[len(list_)-1][0])==0:
                    flag=1
                    break
            if flag==1:
                break

        if flag==1:
            break
        sum+=1
        l1=l
    ans=[]
    prepareans(list_,list_[len(list_)-1],ans,n)
    ans.reverse()
    correctrow(list_,ans,s)
    printans(ans)

n=int(input())
# start=time.time()
l=[]
for i in range(n):
    l.append([])
    temp=input()
    if temp[0]=="(":
        temp=str(temp[1:len(temp)-1]) #去掉最外层的括号
    temp=cutspace(temp)
    temp=cutsign(temp.split())
    l[i].append(temp)
    l[i].append("-1")
    l[i].append("-1")
    l[i].append("")
S=l[:]
resolution(l,S)
# end=time.time()
# print(end-start)