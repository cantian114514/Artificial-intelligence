from sklearn.feature_extraction.text import TfidfVectorizer
import time

def read(file):
    ans=[]
    with open(file,'r') as file_object:
        for line in file_object.readlines():
            temp=line.split()
            ans.append(temp)
    return ans

def distance(a,b): #距离函数
    return ous(a,b)
    # return man_ha(a,b)
    # return cos(a,b)

def ous(a,b): #两个向量之间的欧式距离
    ans=0
    for i in range(0,len(a)):
        # if (a[i]==0 and b[i]!=0) or (a[i]!=0 and b[i]==0):
        #    ans+=1
        ans+=(a[i]-b[i])*(a[i]-b[i])
    ans=ans**0.5
    return ans

def man_ha(a,b): #曼哈顿
    ans=0
    for i in range(0,len(a)):
        if a[i]==b[i]: ans+=0
        else: ans+=1
    return ans

def cos(a,b):
    l1=sum([i**2 for i in a]) **0.5
    l2=sum([i**2 for i in b]) **0.5
    dot_p=sum([a[i]*b[i] for i in range(len(a))])
    ans=dot_p/(l1*l2)
    return ans

def judge(x,arr,emotion,k): #计算测试集中每个用例与训练集中每个用例的距离 选择距离最小的那类感情
    dist=[]
    for i in range(0,len(arr)):
        d=distance(x,arr[i])
        temp=(d,emotion[i])
        dist.append(temp)
    dist=sorted(dist,key=lambda x:x[0])
    x_emotion=[0,0,0,0,0,0]
    for i in range(0,k): #选择前k个最近的样本并根据情感分类
        num=int(dist[i][1])-1
        x_emotion[num]+=1
    ans=x_emotion.index(max(x_emotion))
    return ans+1

if __name__=="__main__":
    start=time.time()

    useless_word="D:\\code\\python\\file\\lab8\\useless.txt"
    file="D:\\code\\python\\file\\lab8\\new_train.txt"
    useless_list=read(useless_word)
    train_list=read(file)
    train_list.pop(0)
    emotion=[]
    example=[]
    for i in range(0,len(train_list)): #分类
        temp_list=train_list[i]
        temp_list=temp_list[3:]
        sentense=""
        for j in range(0,len(temp_list)):
            if temp_list[j] not in useless_list:
                sentense=sentense+temp_list[j]+" " #make sentense
        sentense=sentense[:-1]
        example.append(sentense)
        emotion.append(train_list[i][1]) #一一对应 将单词和情感分开构造后面的独热编码

    tv = TfidfVectorizer(use_idf=False)
    tv_fit = tv.fit_transform(example) #频率
    ft_name = tv.get_feature_names_out() #提取的特征词
    arr = tv_fit.toarray()  #矩阵转列表

    file="D:\\code\\python\\file\\lab8\\new_test.txt"
    test_list=read(file)
    test_list.pop(0)
    test=[]
    for i in range(0,len(test_list)): #分类
        temp_list=test_list[i]
        temp_list=temp_list[3:]
        sentense=""
        for j in range(0,len(temp_list)):
            if temp_list[j] not in useless_list:
                sentense=sentense+temp_list[j]+" " #make sentense
        sentense=sentense[:-1]
        test.append(sentense)

    tv1 = TfidfVectorizer(use_idf=False)
    tv_fit1 = tv.fit_transform(test) #频率
    ft_name1 = tv.get_feature_names_out() #提取的特征词
    arr1 = tv_fit1.toarray()  #矩阵转列表
    
    right=0
    k=16
    for i in range(0,len(test_list)):
        temp=test_list[i]
        answer=int(temp[1])
        ss=temp[3:]
        judgement=judge(arr1[i],arr,emotion,k)
        if judgement==answer:
            right+=1
        print("第",i+1,"句判断为:",judgement,",答案为:",answer,",用例为:",ss)
    ans=(right/len(test_list))*100
    print("正确率为：",ans,"%")
    end=time.time()
    print("耗时：",end-start)