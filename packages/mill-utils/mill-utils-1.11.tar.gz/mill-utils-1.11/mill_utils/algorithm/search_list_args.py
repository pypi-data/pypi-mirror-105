import numpy as np
from tqdm import tqdm

def search_list(func,arg_arr,pop_size=200):
	'''
	搜索参数列表以得到函数最大值
	params:
	--------------
		func: 函数
		arg_arr: array, 参数列表
	
	return:  (搜索到的参数, 对应的最大值)
		
	示例:
	--------------------
		search_list(np.cos,np.arange(0,1,0.1))
		>>> (0.0, 1.0)
	
	
		from itertools import product
		a = np.arange(-3,3,0.1)
		arg_arr = np.array(list(product(a,a)))
		search_list(F,arg_arr)
	
		>>> (array([2.66453526e-15, 1.60000000e+00]), array([7.14022745]))
	'''
    l = len(arg_arr) # 参数列表的长度
    iter_num = np.ceil(l/pop_size)   # 计算迭代次数
    max_args = None  # 最大结果对应的参数
    max_result = None # 最大结果
    dim = 1 if len(arg_arr.shape)==1 else arg_arr.shape[1] # 参数个数
    for i in tqdm(range(int(iter_num))):
        batch_args = arg_arr[i*pop_size:(i+1)*pop_size]    # 本批次参数
        if dim ==1:  # 只有一个参数
            results = func(batch_args)                     # 计算结果
        else:        # 多个参数
            batch_args1 = np.array_split(batch_args, dim,axis=1)
            results = func(*batch_args1)                   # 计算结果
        batch_max_idx = np.argmax(results)                 # 最大结果索引
        batch_max_result = results[batch_max_idx]          # 最大结果
        if max_result==None or batch_max_result > max_result: # 第一次迭代或者最大结果大于缓存
            max_result=batch_max_result                    # 缓存最大结果
            max_args=batch_args[batch_max_idx]             # 缓存最大参数
    return max_args,max_result