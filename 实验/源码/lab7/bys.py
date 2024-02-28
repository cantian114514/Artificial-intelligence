from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import time

def read(file):
    ans=[]
    with open(file,'r',encoding='utf-8') as file_object:
        for line in file_object.readlines():
            temp=line.split()
            ans.append(temp)
    return ans

def lpls(res,k):
    sum=0
    for i in range(0,len(res)):
        sum=0 #每到一个新的行都要更新
        for j in range(0,len(res[i])):
            sum+=res[i][j]
        for j in range(len(res[i])):
            res[i][j]=(res[i][j]+k)/(sum+len(res[0])*k)
    return res

def extend(res):
    for i in range(0,len(res)):
        for j in range(0,len(res[0])):
            res[i][j]*=10000000000
    return res

def classify(set):
    tv=TfidfVectorizer(use_idf=True)
    tv_fit=tv.fit_transform(set)
    ft_name = tv.get_feature_names_out()
    res = tv_fit.toarray()
    res=lpls(res,0.000114514)
    res_norm = np.array(res) / np.sum(res,axis=1,keepdims=True)
    res_norm=extend(res_norm)
    arr.append(res_norm)
    word.append(ft_name)

def find(name,index):
    for i in range(0,len(name)):
        if name[i]==index:
            return i

def judge(num,arr,ss,word):
    res=0
    for i in range(0,len(arr[num])):
        mul=1
        for j in range(0,len(ss)):
            if ss[j] in word[num]:
                index=find(word[num],ss[j])
                mul*=arr[num][i][index] #后验概率公式
        res+=mul
    return res

if __name__=='__main__':
    start=time.time()
    useless_word="D:\\code\\python\\file\\lab7\\useless.txt"
    file="D:\\code\\python\\file\\lab7\\train.txt"
    # useless_list=[]
    useless_list=read(useless_word)
  
    train_list=read(file)
    train_list.pop(0)
    
    anger_=[] #1
    disgust_=[] #2
    fear_=[] #3
    joy_=[] #4
    sad_=[] #5
    surprise_=[] #6

    for i in range(0,len(train_list)): #分类
        temp_list=train_list[i]
        temp_list=temp_list[3:]
        sentense=""
        for j in range(0,len(temp_list)):
            if temp_list[j] not in useless_list:
                sentense=sentense+temp_list[j]+" " #make sentense
        sentense=sentense[:-1]

        if train_list[i][1]=='1':
            anger_.append(sentense)
        elif train_list[i][1]=='2':
            disgust_.append(sentense)
        elif train_list[i][1]=='3':
            fear_.append(sentense)
        elif train_list[i][1]=='4':
            joy_.append(sentense)
        elif train_list[i][1]=='5':
            sad_.append(sentense)
        elif train_list[i][1]=='6':
            surprise_.append(sentense)

    # print(len(anger_))
    arr=[]
    word=[]
    classify(anger_)
    classify(disgust_)
    classify(fear_)
    classify(joy_)
    classify(sad_)
    classify(surprise_)
    #分类完成-------------------------------------
    file="D:\\code\\python\\file\\lab7\\test.txt"
    test_list=read(file)
    test_list.pop(0)
    right=0
    for i in range(0,len(test_list)):
        temp=test_list[i]
        answer=int(temp[1])
        ss=temp[3:]
        max=-100000
        judgement=-1
        for j in range(6):
            res=judge(j,arr,ss,word)
            if res>max:
                max=res
                judgement=j+1
        if judgement==answer:
            right+=1
        print("第",i+1,"句判断为:",judgement,",答案为:",answer,",用例为:",ss)
    ans=(right/len(test_list))*100
    print("正确率为：",ans,"%")

    end=time.time()
    print(end-start)