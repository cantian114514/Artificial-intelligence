from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np 

tv = TfidfVectorizer(use_idf=False)
text = ['Step by step we will succeed','We step on shit']
tv_fit = tv.fit_transform(text)
# print(tv_fit)
ft_name = tv.get_feature_names_out()
print(ft_name)
# print(" ")
# res = tv_fit.toarray()
# print(res)
# print(" ")
# res_norm = np.array(res) / np.sum(res,axis=1,keepdims=True)
# print(res_norm)
# 定义词汇表
# 计算平滑后的矩阵