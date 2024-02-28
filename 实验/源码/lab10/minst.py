import numpy as np
import struct
import matplotlib.pyplot as plt
import math
from tqdm import trange

train_label=[]
test_label=[]
train_list=[]
test_list=[]

#解析代码参考博客https://blog.csdn.net/lindorx/article/details/94639183
def decode_idx3_ubyte(file):#此函数用来解析idx3文件，idx3_ubyte_filec指定图像文件路径
    """
    images是一个三维数组,images[i][a][b]表示第i张图片的倒数第a行,b列的像素
    """
    #读取二进制数据
    bin_data=open(file,'rb').read()
    #解析文件头信息，依次为魔数、图片数量、每张图片高、每张图片宽
    offest=0
    fmt_header='>iiii'    
    magic_num,num_images,num_rows,num_cols=struct.unpack_from(fmt_header,bin_data,offest)
    print(magic_num,num_images,num_rows,num_cols)
    #解析数据集
    offest += struct.calcsize(fmt_header)
    fmt_image='>'+str(num_rows*num_cols)+'B'
    images=np.empty((num_images,num_rows,num_cols))
    for i in range(num_images):      
        images[i]=np.array(struct.unpack_from(fmt_image,bin_data,offest)).reshape((num_rows,num_cols))
        offest+=struct.calcsize(fmt_image)
    
    return images

def decode_idx1_ubyte(file):#解析idx1文件函数，idx1_ubyte_file指定标签文件路径
    """
    labels是一个一维数组,每个元素都一一对应images[i]
    """
    #读取二进制数据
    bin_data=open(file,'rb').read()
    #解析文件头信息，依次为魔数和标签数
    offest=0
    fmt_header='>ii'
    magic_num,num_images=struct.unpack_from(fmt_header,bin_data,offest)
    print(magic_num,num_images)
    #解析数据集
    offest += struct.calcsize(fmt_header)
    fmt_image='>B'
    labels=np.empty(num_images)
    for i in range(num_images):
        labels[i]=struct.unpack_from(fmt_image,bin_data,offest)[0]
        offest+=struct.calcsize(fmt_image)

    return labels

def initialization():
    # MNIST数据集中的图片和标签数据是按照大端字节序存储
    file=[  "D:\\code\\python\\file\\lab10\\minst\\train-images.idx3-ubyte", # 训练集图像 用坐标来表示 大小从0~255 长28宽28
            "D:\\code\\python\\file\\lab10\\minst\\train-labels.idx1-ubyte", # 跟图片对应的标签
            "D:\\code\\python\\file\\lab10\\minst\\t10k-images.idx3-ubyte",
            "D:\\code\\python\\file\\lab10\\minst\\t10k-labels.idx1-ubyte"]
    data_set=[decode_idx3_ubyte(file[0]),decode_idx3_ubyte(file[2])]
    train_label=[decode_idx1_ubyte(file[1])][0]
    test_label=[decode_idx1_ubyte(file[3])][0]
    
    #将图片矩阵转换成行向量，方便计算
    for i in range(0,len(data_set[0])): #60000
        train_list.append(data_set[0][i].reshape(784,)/255)
    for i in range(0,len(data_set[1])): #10000
        test_list.append(data_set[1][i].reshape(784,)/255)

    # 学习率
    a1=0.2
    a2=0.2
    #权重初始化
    w1=np.random.uniform(-0.5,0.5,(784,100)) # 输入层结点数 & 隐藏层结点数
    w2=np.random.uniform(-0.5,0.5,(100,10)) # 隐藏层结点数 & 输出层结点数（0~9）
    #偏置向量初始化
    b1=[0 for _ in range(0,100)]
    b2=[0 for _ in range(0,10)]

    return train_list,train_label,test_list,test_label,a1,a2,b1,b2,w1,w2

def sigmoid(z):
    ans=[]
    for i in range(0,len(z)):
        e_z=math.exp(-z[i])
        ans.append(1/(1+e_z))
    return np.array(ans)

def train(a1,a2,b1,b2,w1,w2,loss):
    for i in trange(0,len(train_list)):
        hide=np.dot(train_list[i],w1)+b1
        hide_ans=sigmoid(hide)

        output=np.dot(hide_ans,w2)+b2
        output_ans=sigmoid(output)

        real_ans=np.array([0 for _ in range(0,10)])
        real_ans[int(train_label[i])]=1

        # 更新参数
        e2=real_ans-output_ans
        dt_output=output_ans*(1-output_ans)*e2 #三个同维向量相乘 注意这里不能拆开到循环中来乘
        e1=np.dot(w2,e2) #e1通过e2倒推回去 回到100*1的状态 虽然不是完全符合的值但是接近
        dt_hide=hide_ans*(1-hide_ans)*e1

        for j in range(0,10):
            w2[:,j]+=a2*dt_output[j]*hide_ans
        for j in range(0,100):
            w1[:,j]+=a1*dt_hide[j]*train_list[i]

        b2+=a2*dt_output
        b1+=a1*dt_hide
        if i%100==0:
            loss.append(abs(np.mean(e2)))

def test(b1,b2,w1,w2):
    right=0
    all=len(test_list)
    for i in range(0,len(test_list)):
        hide_ans=sigmoid(np.dot(test_list[i],w1)+b1)
        output_ans=sigmoid(np.dot(hide_ans,w2)+b2).tolist()
        test_ans=output_ans.index(max(output_ans))
        real_ans=int(test_label[i])
        if test_ans==real_ans:
            right+=1
        print("example ",i,": test result is:",test_ans,", correct result is:",real_ans)
    print("Rate:",right/all*100,"%")

if __name__=="__main__":
    train_list,train_label,test_list,test_label,a1,a2,b1,b2,w1,w2=initialization()
    #损失函数
    loss=[]
    train(a1,a2,b1,b2,w1,w2,loss)
    test(b1,b2,w1,w2)

    x=[i for i in range(0,len(loss))]
    plt.plot(x,loss)
    plt.title("loss graph")
    plt.show()