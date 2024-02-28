import torch
import numpy as np
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt

batch_size=128 # https://aistudio.baidu.com/aistudio/projectdetail/5738888
# https://blog.csdn.net/qq_25426559/article/details/122263705
class dataset(DataLoader): 
    def __init__(self,file):
        self.file=file
        self.img=[]
        f=open(file,'r',encoding='utf-8')
        for img_info in f:
            example=img_info.rstrip()
            example=example.split('!')
            self.img.append((example[0],int(example[1])))
    def __getitem__(self,index):
        img_path,label=self.img[index]
        image=Image.open(img_path)
        if image.mode!='RGB': 
            image=image.convert('RGB')
        image=image.resize((128,128),Image.BILINEAR)
        image=np.array(image).astype('float32')
        image=image.transpose((2,0,1))/255
        label=np.array([label],dtype='int64')
        return image,label
    def __len__(self):
        return len(self.img)

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1=nn.Sequential(
            nn.Conv2d(in_channels=3,out_channels=32,kernel_size=3,stride=1,padding=1),#卷积
            nn.BatchNorm2d(32),         
            nn.ReLU(inplace=True),#激活函数
            nn.Conv2d(32,32,5,1,2),
            nn.BatchNorm2d(32),         
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2,stride=2),#池化
        )
        self.conv2=nn.Sequential(
            nn.Conv2d(32,64,3,1,1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64,64,3,1,1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2,2),
        )
        self.conv3=nn.Sequential(
            nn.Conv2d(64,128,3,1,1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128,128,3,1,1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2,2),
        )
        self.conv4=nn.Sequential(
            nn.Conv2d(128,256,3,1,1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256,256,3,1,1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2,2),
        )
        self.classify=nn.Sequential(
            nn.Dropout(0.5), #防止过拟合
            nn.Linear(256*8*8,256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),

            nn.Dropout(0.5),
            nn.Linear(256,128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),

            nn.Dropout(0.5),
            nn.Linear(128,5),
            nn.BatchNorm1d(5),
            nn.ReLU(inplace=True),
        )
    def forward(self,x):
        x=self.conv1(x)
        x=self.conv2(x)
        x=self.conv3(x)
        x=self.conv4(x)
        x=x.flatten(1) #展平成一维向量
        x=self.classify(x)
        return x
    
def data_processing():
    train_data = dataset('D:\\code\\python\\file\\lab11\\alltrain.txt')
    test_data = dataset('D:\\code\\python\\file\\lab11\\alltest.txt')
    train_loader = DataLoader(train_data,batch_size=batch_size,shuffle=True)
    test_loader = DataLoader(test_data,batch_size=batch_size,shuffle=False)
    return train_loader, test_loader
    
def test(net):
    correct=0
    total=0
    with torch.no_grad():
        for _,(x,y) in enumerate(test_loader):
            x=x.reshape(-1,3,128,128)
            outputs=net(x)
            _,pred=torch.max(outputs.data,dim=1)
            pred=pred.reshape(10,1)
            total+=y.size(0)
            correct+=(pred==y).sum().item()
            # print("pred:",pred,"label:",y)
    return correct/total

def train(net,criterion,optim,epochs):
    net.train()
    loss=[]
    accuracy=[]
    for epoch in range(epochs):
        for step,(input,label) in enumerate(train_loader):
            input=input.reshape(-1,3,128,128)
            output=net(input)
            loss_one=criterion(output,label.squeeze(dim=1))
            optim.zero_grad() #在更新前清除上一步的梯度
            loss_one.backward() #loss反向传播
            optim.step() #优化器更新
            loss.append(loss_one.item()) #损失值记录
            rate=test(net)
            accuracy.append(rate)
            print("epoch:",epoch,"data id:",step+1,"loss:",loss_one.item(),"accuracy:",rate)
    x=[i for i in range(0,len(loss))]
    p1=plt.figure(1)
    plt.plot(x,loss)
    plt.title("loss graph")
    p2=plt.figure(2)
    plt.plot(x,accuracy)
    plt.title("accuracy graph")
    plt.show()

if __name__=="__main__":
    train_loader,test_loader=data_processing()
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net=CNN().to(device) # 定义网络
    criterion=torch.nn.CrossEntropyLoss() #定义损失函数
    optim=torch.optim.Adam(net.parameters(),lr=1e-3) #定义网络优化器
    epochs=20 # 定义epoch
    train(net,criterion,optim,epochs)