from django.test import TestCase

# Create your tests here.



def maxnum(input_str):
    if input_str:
        str_list = input_str.split(',')
        for i in range(len(str_list)-1):
            for j in range(len(str_list)-1-i):
                if len(str_list[j])>len(str_list[j+1]):
                    str_list[j],str_list[j+1]=str_list[j+1],str_list[j]
        return str_list[-1]
    else:
        return None

print(maxnum('asad,dskadskdakdks,sdjsdkajd,jsjasjk'))

max_len = maxnum('asad,dskadskdakdks,sdjsdkajd,jsjasjk')
def is_need(max_str):
    if max_str:
        for i in ['a','e','i','o','u']:
            if i in max_str:
                pass

# 方法一：
# def count_str(test_str):
#     try:
#         output=[]
#         for i in test_str:
#             # 先去重
#             if i not in output:
#                 output.append(i)
#         # 再计算每一个字符出现的次数
#         for j in output:
#             print(f'{j}出现次数为：{test_str.count(j)}')
#     except Exception as e:
#         print(e)

def count_str(test_str):
    try:
        # 创建空字典
        dict1={}
        for i in test_str:
            # 判断字典中是否存在该字符，如果存在value+1，否则value=1
            if i in dict1:
                dict1[i]+=1
            else:
                dict1[i]=1
        # 遍历字典去除key和value
        for k,v in dict1.items():
            print(f'{k}出现次数为：{v}')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    count_str('aabbccddee123AZDEDFASFSF.,$%@#&^KMza1235+')
