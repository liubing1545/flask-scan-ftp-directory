import os


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if not os.path.isdir(tmp_path):
            print('file: %s'%tmp_path)
        else:
            print('folder:%s'%tmp_path)
            traverse(tmp_path)

path = 'E:\drive\G71-MAD1045'
traverse(path)