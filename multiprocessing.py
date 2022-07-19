import os
from multiprocessing import Process

def run_a_sub_proc(name):
    print(f'子进程：{name}（{os.getpid()}）开始...')

if __name__ == '__main__':
    print(f'主进程（{os.getpid()}）开始...')
    # 通过对Process类进行实例化创建一个子进程
    p = Process(target=run_a_sub_proc, args=('测试进程', ))
    p.start()
    p.join()