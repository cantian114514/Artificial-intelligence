import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from matplotlib import pyplot as plt
from torch.utils.data import TensorDataset

class AutoEncoder(torch.nn.Module):
    def __init__(self):
        super(AutoEncoder,self).__init__()
        # 编码器 学习特征
        self.encoder=torch.nn.Sequential( # [b,784]->[b,36]
            torch.nn.Linear(784,256),
            torch.nn.ReLU(),
            torch.nn.Linear(256,128),
            torch.nn.ReLU(),
            torch.nn.Linear(128,36),
            torch.nn.ReLU()
        )
        # 解码器 生成
        self.decoder=torch.nn.Sequential( # [b,36]->[b,784]
            torch.nn.Linear(36,128),
            torch.nn.ReLU(),
            torch.nn.Linear(128,256),
            torch.nn.ReLU(),
            torch.nn.Linear(256,784),
            torch.nn.Sigmoid()
        )
    def forward(self, x):
        batch_size=x.size(0) # x:[b,1,28,28]
        x=x.view(batch_size,-1) # flatten
        x=self.encoder(x) # encoder
        x=self.decoder(x) # decoder
        x=x.view(batch_size,1,28,28) # reshape
        return x
    
    def forward_(self, x):
        batch_size=x.size(0) # x:[b,1,28,28]
        x=x.view(batch_size,-1) # flatten
        x=self.encoder(x) # encoder
        x=x.view(batch_size,1,6,6) # reshape
        return x

class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1=torch.nn.Sequential( # input shape(1,6,6)
            torch.nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=3,
                stride=1,
                padding=2,
            ), #output shape(16,6,6)
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2), # (16,3,3)
        )
        self.conv2=torch.nn.Sequential( #(1,6,6)
            torch.nn.Conv2d(16,32,3,1,2), #(32,3,3)
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2), #(32,3,3)
        )
        self.out=torch.nn.Linear(32 *3 *3,10)

    def forward(self,x):
        x=self.conv1(x)
        x=self.conv2(x)
        x=x.view(x.size(0),-1)
        output=self.out(x)
        return output

def download_data():   # 加载数据集
    train_list=datasets.MNIST(root='mnist',train=True,transform=transforms.Compose([
        transforms.ToTensor()]),download=True)
    train_list=DataLoader(train_list,batch_size=32,shuffle=True)

    test_list=datasets.MNIST(root='mnist',train=True,transform=transforms.Compose([
        transforms.ToTensor()]),download=True)
    test_list=DataLoader(test_list,batch_size=32,shuffle=False)

    return train_list, test_list

def data_processing(): #用AE提取特征 并压缩为loader
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    with torch.no_grad():
        for data in train_list:
            inputs, labels = data
            encoded = net.forward_(inputs.view(inputs.size(0), -1))
            train_features.append(encoded)
            train_labels.append(labels)
        for data in test_list:
            inputs, labels = data
            encoded = net.forward_(inputs.view(inputs.size(0), -1))
            test_features.append(encoded)
            test_labels.append(labels)
    # 合并成一维
    train_features = torch.cat(train_features, dim=0).numpy()
    train_labels = torch.cat(train_labels, dim=0).numpy()
    test_features = torch.cat(test_features, dim=0).numpy()
    test_labels = torch.cat(test_labels, dim=0).numpy()

    train_features = torch.from_numpy(train_features).float()
    train_labels = torch.from_numpy(train_labels).long()
    test_features = torch.from_numpy(test_features).float()
    test_labels = torch.from_numpy(test_labels).long()

    train_dataset = TensorDataset(train_features, train_labels)
    train_loader = DataLoader(train_dataset, batch_size=10, shuffle=True)
    test_dataset = TensorDataset(test_features, test_labels)
    test_loader = DataLoader(test_dataset, batch_size=10, shuffle=False)
    return train_loader,test_loader

def train1(net,criterion,optim,epochs):
    loss=[]
    for epoch in range(epochs):
        for batch_id,(input,_) in enumerate(train_list):
            net.train()
            output=net(input)
            loss_one=criterion(output,input)
            optim.zero_grad() #在更新前清除上一步的梯度
            loss_one.backward() #loss反向传播
            optim.step() #优化器更新
            loss.append(loss_one.item()) #损失值记录
            print("TRAIN 1 epoch:",epoch,"data id:",batch_id+1,"loss:",loss_one.item())
    x=[i for i in range(0,len(loss))]
    plt.plot(x,loss)
    plt.title("loss graph")
    plt.show()

def test1(goal):
    net.eval()# 停止反向传播
    data=iter(test_list)
    input,labels=next(data)
    with torch.no_grad(): output=net(input)
    id=0
    while 1:
        for i in range(32): # label维度是32
            if labels[i]==goal:
                plt.subplot(2,10,id+1)
                plt.imshow(input[i].numpy().squeeze(), cmap='gray_r')
                plt.xticks([])
                plt.yticks([])
                plt.subplot(2,10,id+11)
                plt.imshow(output[i].numpy().squeeze(), cmap='gray_r')
                plt.xticks([])
                plt.yticks([])
                id+=1
            if id==10: break 
        if id==10: break
        else:
            input,labels=next(data)
            with torch.no_grad(): output=net(input)
    plt.show()

def test2(net):
    correct=0
    total=0
    with torch.no_grad():
        for _,(x,y) in enumerate(test_loader):
            outputs=net(x)
            _,pred=torch.max(outputs.data,dim=1)
            total+=y.size(0)
            correct+=(pred==y).sum().item()
    return correct/total

def train2(cnn,criterion,optimizer,epochs):
    accuracy=[]
    for epoch in range(epochs):
        for step,(x,y) in enumerate(train_loader):
            output=cnn(x)
            loss=criterion(output,y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print("TRAIN 2,epoch:",epoch,"data id:",step+1,"loss:",loss.item())
            if step%50==0:
                rate=test2(cnn)
                accuracy.append(rate)
    x=[i for i in range(0,len(accuracy))]
    plt.plot(x,accuracy)
    plt.title("accuracy graph")
    plt.show()

if __name__=="__main__":
    train_list, test_list=download_data()
    epochs=1 #epochs次数
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net=AutoEncoder().to(device)
    criterion=torch.nn.MSELoss() #定义损失函数
    optim=torch.optim.Adam(net.parameters(),lr=1e-3) #定义网络优化器
    train1(net,criterion,optim,epochs)
    test1(6)

    train_loader,test_loader=data_processing()
    cnn=CNN().to(device)
    criterion=torch.nn.CrossEntropyLoss()
    optimizer=torch.optim.Adam(cnn.parameters(),lr=1e-3)
    train2(cnn,criterion,optimizer,epochs)