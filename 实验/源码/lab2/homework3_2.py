import math
import time
tail=["(x,y)","(x,z)","(y,x)","(y,z)","(z,x)","(z,y)"]
def get_front_case(eg): #取双例的前部分
    return eg[eg.find("(")+1:eg.find(",")]

def get_behind_case(eg): #取单例的后部分
    return eg[eg.find(",")+1:eg.find(")")]

def isvar(f): #判断是否是变量
    if f in['x','y','z','u','v','w']: return True
    else: return False

def get_gainvalue(n_t:int,n_f:int,o_t:int,o_f:int): #计算增益值
    if n_t==0: return -1
    front=math.log2(n_t/(n_t+n_f))
    behind=math.log2(o_t/(o_t+o_f))
    ans=o_t*(front-behind)
    return ans

def get_backgront_knowledge(n:int): #最开始的输入
    bk=[]
    for i in range(n):
        a=input()
        bk.append(a)
    return bk

def get_train_knowledge(bk:list,goal:str): #初始化训练集合
    ans=[]
    j=0
    for j in range(0,len(bk)):
        if bk[j][:bk[j].find("(")]==goal[:goal.find("(")]:
            ans.append(bk[j])
            break
    g_head="¬"+goal[:goal.find("(")] #头部取否 创造反例
    for i in range(0,len(bk)):
        if i!=j:
            t=g_head+bk[i][bk[i].find("("):len(bk[i])]
            ans.append(t)
    return ans

def get_train_example(bk:list,goal:str): #得到前提约束谓词集
    have_use=[]
    ans=[]
    goal_head=goal[:goal.find("(")]
    for i in range(0,len(bk)):
        head=bk[i][:bk[i].find("(")]
        if head!=goal_head:
            if len(have_use)==0 or have_use.count(head)==0:
                have_use.append(head)
                for j in range(0,6):
                    t=str(head+tail[j])
                    ans.append(t)
    return ans

def meta(train,eg): #判断两个例子可判为正例或反例
    if train==eg: 
        return True
    else:
        x1=get_front_case(eg)
        x2=get_behind_case(eg)
        if isvar(x1)==True:
            x3=get_behind_case(train)
            if x2==x3: return True
            else: return False
        elif isvar(x2)==True:
            x3=get_front_case(train)
            if x1==x3: return True
            else: return False
        else: return False

def replace_f(tr_e,bk,t_replace): #算正反例时用到的替换函数
    x1=get_front_case(tr_e)
    x1_eg=get_front_case(bk)
    x2=get_behind_case(tr_e)
    x2_eg=get_behind_case(bk)
    t_replace=t_replace.replace(x1,x1_eg)
    t_replace=t_replace.replace(x2,x2_eg)
    return t_replace

def get_m_true(tr_e,traink,bk,goal): #计算正例数
    if len(goal)==1:
        for i in range(0,len(bk)):
            if bk[i][:bk[i].find("(")]==tr_e[:tr_e.find("(")]:
                t_replace=goal[0][:]
                t_replace=replace_f(tr_e,bk[i],t_replace)
                #然后在训练集中查找正反例 这里只用看第一个训练式
                flag=meta(traink[0],t_replace)
                if flag==True: return 1
        return 0
    elif len(goal)==2:
        for i in range(0,len(bk)):
            if bk[i][:bk[i].find("(")]==tr_e[:tr_e.find("(")]:
                t1=goal[1][:]
                t1=replace_f(tr_e,bk[i],t1)
                for j in range(0,len(bk)):
                    flag=meta(bk[j],t1)
                    if flag==True:
                        t2=goal[0][:]
                        t2=replace_f(tr_e,bk[i],t2)
                        flag1=meta(traink[0],t2)
                        if flag1==True:return 1
        return 0
    return 0

def get_m_false(tr_e,traink,bk,goal): #计算反例数
    ans=0
    use=[]
    if len(goal)==1:
        for i in range(0,len(bk)):
            if bk[i][:bk[i].find("(")]==tr_e[:tr_e.find("(")]:
                t_replace=goal[0][:]
                t_replace=replace_f(tr_e,bk[i],t_replace)
                t_replace="¬"+t_replace
                if use.count(t_replace)==0:  #已经检查过的例子就不再使用
                    use.append(t_replace) 
                    #然后在训练集中查找正反例 这里只用看第一个训练式
                    for j in range(1,len(traink)):
                        flag=meta(traink[j],t_replace)
                        if flag==True: 
                            ans+=1
        return ans
    elif len(goal)==2:
        for i in range(0,len(bk)):
            if bk[i][:bk[i].find("(")]==tr_e[:tr_e.find("(")]:
                t1=goal[1][:]
                t1=replace_f(tr_e,bk[i],t1)
                for j in range(0,len(bk)):
                    flag=meta(bk[j],t1)
                    if flag==True:
                        t2=goal[0][:]
                        t2=replace_f(tr_e,bk[i],t2)
                        t2="¬"+t2
                        flag1=meta(traink[1],t2)
                        if flag1==True: return 1
        return 0
    return 0

def cut_traink(traink,new_eg,goal): #更新训练集
    if len(traink)==2: return traink
    x1=get_front_case(new_eg)
    y1=get_behind_case(new_eg)
    x2=get_front_case(goal)
    y2=get_behind_case(goal)
    if x1==x2:
        eg=get_front_case(traink[0])
        n=len(traink)
        i=1
        while i<n:
            eg_check=get_front_case(traink[i])
            if eg_check!=eg:
                del traink[i]
                n-=1
                i-=1
            i+=1
    elif y1==y2:
        eg=get_behind_case(traink[0])
        n=len(traink)
        i=1
        while i<n:
            eg_check=get_behind_case(traink[i])
            if eg_check!=eg:
                del traink[i]
                n-=1
                i-=1
            i+=1
    return traink

def print_ans(goal,bk):  #按输出格式打印答案
    ss=""
    for i in range(1,len(goal)):
        if i==len(goal)-1:
            ss+=goal[i]+" → "+goal[0]
        else:
            ss+=goal[i]+" ∧ "
    print(ss)
    ans=[]
    for i in range(0,len(bk)-1):
        x1=get_front_case(bk[i])
        y1=get_behind_case(bk[i])
        for j in range(i+1,len(bk)):
            x2=get_front_case(bk[j])
            y2=get_behind_case(bk[j])
            if x2==y1:
                a=goal[0][:]
                a=a.replace(get_front_case(a),x1)
                a=a.replace(get_behind_case(a),y2)
                if bk.count(a)==0:
                    ans.append(a)
    for i in range(0,len(ans)):
        print(ans[i])
            

n=int(input())
bk=get_backgront_knowledge(n)
goal0=str(input())
goal=[goal0]
# start=time.time()
traink=get_train_knowledge(bk,goal[0])
train_example=get_train_example(bk,goal[0])
o_t=1
o_f=len(traink)-1
n_t=n_f=0
use=[]
while o_f!=0 or o_t!=1:
    min=-1
    for i in range(0,len(train_example)):
        if use.count(train_example[i])!=0:
            continue
        t1=n_t
        t2=n_f
        n_t=get_m_true(train_example[i],traink,bk,goal)
        n_f=get_m_false(train_example[i],traink,bk,goal)
        if n_t==0: continue
        else:
            gainvalue=get_gainvalue(n_t,n_f,o_t,o_f)
            if gainvalue>min:
                new_eg=train_example[i]
                t1=n_t
                t2=n_f
                min=get_gainvalue(n_t,n_f,o_t,o_f)
    traink=cut_traink(traink,new_eg,goal[0])
    o_t=get_m_true(new_eg,traink,bk,goal)
    o_f=get_m_false(new_eg,traink,bk,goal)
    goal.append(new_eg)
    use.append(new_eg)
print_ans(goal,bk)
# end=time.time()
# print(end-start)