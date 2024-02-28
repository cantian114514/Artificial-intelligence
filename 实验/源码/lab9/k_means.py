from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import random
import numpy as np
import time

c=['#DC143C','#FF00FF','#0000FF','#00FF00','#FFD700','#808080']#六个类的颜色分布

def read(file):
    ans=[]
    with open(file,'r',encoding='utf-8') as file_object:
        for line in file_object.readlines():
            temp=line.split()
            ans.append(temp)
    return ans

def distance(a,b): #两个向量之间的欧式距离
    ans=0
    for i in range(0,len(a)):
        ans+=(a[i]-b[i])*(a[i]-b[i])
    ans=ans**0.5
    return ans

def get_centroid(arr): #算质心
    aver=[0 for i in range(0,len(arr[0]))]
    for i in range(0,len(arr)+1):
        if i==len(arr):
            for j in range(0,len(arr[0])):
                aver[j]/=len(arr) #得到平均值点
        else:
            for j in range(0,len(arr[0])):
                aver[j]+=arr[i][j]
    min=9999999
    ans=arr[0]
    for i in range(0,len(arr)):
        d=distance(aver,arr[i])
        if d<min:
            min=d
            ans=arr[i]
    return ans

def k_means_plus(arr,k): #k-means++ 让初始聚类中心之间的相互距离尽可能远
    first_dot=random.randint(0,len(arr)-1)
    ans=[arr[first_dot]]
    while k-1:
        dis=[] #每次选取都更新数组
        for i in range(0,len(arr)):
            d=0
            for j in range(0,len(ans)):
                d+=distance(ans[j],arr[i]) #根据答案集的大小更改循环次数
            dis.append(d)
        while True:#按概率采样一个样本点，距离越大，被采样的概率也就越大
            dot=random.choices(arr,dis,k=1) #轮盘赌
            if dot not in ans:
                ans.append(dot[0])
                break
        k-=1
    return ans

def judgement(arr,k,dot): #每一次根据原来的质心计算分类 并算新的质心
    classify=[[],[],[],[],[],[]]
    label=[]
    new_dot_set=[]
    d=[0,0,0,0,0,0]
    #通过距离分类
    for i in range(0,len(arr)):
        d=[0,0,0,0,0,0]
        for j in range(0,k):
            d[j]=distance(arr[i],dot[j]) #计算并存入与每个质心的距离
        temp=d.index(min(d))
        classify[temp].append(arr[i]) #聚类
        label.append(temp)
    #计算新的质心
    for i in range(0,k):
        t=get_centroid(classify[i])
        new_dot_set.append(t)
    return label,classify,new_dot_set

def k_means(arr,k):
    dot_set=k_means_plus(arr,k)
    new_dot_set=[]
    for i in range(0,800):
        label,classify,new_dot_set=judgement(arr,k,dot_set)
        dot_set=new_dot_set
    return label,classify,dot_set

def dimension_reduction(X_): #https://blog.csdn.net/qq_41076797/article/details/115508184
    tsne2d=TSNE(n_components=2,perplexity=1,init='pca',random_state=0)
    X=np.array(X_)
    X_tsne_2d=tsne2d.fit_transform(X)
    x_min, x_max=np.min(X_tsne_2d,0),np.max(X_tsne_2d,0)
    ans=(X_tsne_2d-x_min)/(x_max-x_min)
    return ans

if __name__=="__main__":
    useless_word="D:\\code\\python\\file\\lab9\\useless.txt"
    file="D:\\code\\python\\file\\lab9\\train.txt"
    useless_list=read(useless_word)
    train_list=read(file)
    train_list.pop(0)
    start=time.time()

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
    
    #构建向量空间模型 提取特征词
    tv = TfidfVectorizer(use_idf=False)
    tv_fit = tv.fit_transform(example) #频率
    ft_name = tv.get_feature_names_out() #提取的特征词
    arr = tv_fit.toarray().tolist()  #矩阵转列表
    
    arr=dimension_reduction(arr).tolist() #先降维再分类 不然投影图会混成一团，可以与下面那个降维对比
    label,classify,dot=k_means(arr,6) #6种情感 label是分类后对应arr中每条的分类结果

    score=metrics.calinski_harabasz_score(arr,label)
    print("分出为六类的情况下 Calinski-Harabasz Score为:",score) 
    #https://blog.csdn.net/qq_27825451/article/details/94436488?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~aggregatepage~first_rank_ecpm_v1~rank_v31_ecpm-1-94436488.pc_agg_new_rank&utm_term=DBI%E6%8C%87%E6%A0%87%20sklearn&spm=1000.2123.3001.4430

    # for i in range(0,6):
    #     classify[i]=dimension_reduction(classify[i]) #先分类再降维

    end=time.time()
    print("用时：",end-start)

    #可视化
    for i in range(0,6):
        x=[]
        y=[]
        for j in range(0,len(classify[i])):
            x.append(classify[i][j][0])
            y.append(classify[i][j][1])
        plt.scatter(x,y,marker='o',s=50,color=c[i])
    plt.title('K-means graph')
    plt.show()