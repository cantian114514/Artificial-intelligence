import random
def read(file,ans):
    with open(file,'r') as file_object:
        for line in file_object.readlines():
            temp=line.split()
            if temp[0]=="document": continue
            ans.append(temp[1:])
    return ans

def get_str(l):
    ans=""
    for i in range(0,len(l)):
        ans+=l[i]+" "
    return ans[:-1]

file1="D:\\code\\python\\file\\lab8\\test.txt"
file2="D:\\code\\python\\file\\lab8\\train.txt"

sample=[]
sample=read(file1,sample)
sample=read(file2,sample)
length=(len(sample)//10)*8 #训练集的数据
test_new=[]
train_new=[]
num=[]

sum=1
i=length
while i>0:
    temp=random.randint(0,len(sample)-1)
    if temp in num:
        continue
    else:
        num.append(temp)
        ex=str(sum)+" "+get_str(sample[temp])
        train_new.append(ex)
        sum+=1
        i-=1

for i in range(0,len(sample)):
    if i not in num:
        ex=str(sum)+" "+get_str(sample[i])
        #print(sample[i])
        test_new.append(ex)
        sum+=1

file="D:\\code\\python\\file\\lab8\\new_test.txt"
with open(file,'w') as file_object:
    file_object.write("document Id emotion words\n")
    for i in range(0,len(test_new)):
        file_object.write(test_new[i])
        if i!=len(test_new)-1:
            file_object.write('\n')

file="D:\\code\\python\\file\\lab8\\new_train.txt"
with open(file,'w') as file_object:
    file_object.write("document Id emotion words\n")
    for i in range(0,len(train_new)):
        file_object.write(train_new[i])
        if i!=len(train_new)-1:
            file_object.write('\n')

print("finish work")