import time
import os
import re
from multiprocessing import Process


#多进程同时对一个文件进行写操作
def func(x, y, i):
    with open(x, 'a', encoding='utf-8') as f:
        print('当前进程 %5s 拿到的文件的光标位置 >> %s' % (os.getpid(), f.tell()))
        f.write(y)


#多进程同时创建多个文件
# def func(x, y):
#     with open(x, 'w', encoding='utf-8') as f:
#         f.write(y)

if __name__ == '__main__':

    p_list = []
    for i in range(10):
        p = Process(target=func, args=('data/can_do_girl_lists.txt', '姑娘%s' % i, i))
        # p = Process(target=func,args=('can_do_girl_info%s.txt'%i,'姑娘电话0000%s'%i))
        p_list.append(p)
        p.start()

    [ap.join() for ap in p_list]  #这就是个for循环，只不过用列表生成式的形式写的
    with open('data/can_do_girl_lists.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        all_num = re.findall('\d+',
                             data)  #打开文件，统计一下里面有多少个数据，每个数据都有个数字，所以re匹配一下就行了
        print('>>>>>', all_num, '.....%s' % (len(all_num)))
    #print([i in in os.walk(r'你的文件夹路径')])
    print('不要钱~~~~~~~~~~~~~~~~！')