import os
import math
import shutil
import collections
import torch
import torchvision

data_dir = 'D:/毕业设计/classify-leaves'
fname = os.path.join(data_dir, 'train.csv')
# 采用with打开文件
with open(fname, 'r') as f:
    lines = f.readlines()[1:]  # 从1开始,，去掉跳过文件头行 (列名)
    # print(lines)

# lines中有图片的地址和对应的标签。我将lines中每一个数据集去掉空格，并分开每个
# 列表存入，最后放在一个字典中返回（字典最后可以根据图片地址找到相应标签）
def read_csv_train(fname):
    """读取 `fname` 来给标签字典返回一个文件名。"""
    with open(fname, 'r') as f:
        # 跳过文件头行 (列名)
        lines = f.readlines()[1:]
    tokens = [l.rstrip().split(',') for l in lines]  #去掉空格，并分开每个训练图片，列表存入
    return dict(((name, label) for name, label in tokens)) #字典返回返回
labels = read_csv_train(os.path.join(data_dir, 'train.csv'))
# print(labels)
# 同train一样with读取csv文件，但是test的内容和train不一样，里面没有标签
fname = os.path.join(data_dir, 'test.csv')
with open(fname, 'r') as f:
    # 跳过文件头行 (列名)
    lines = f.readlines()[1:]
    # print(lines)

#只需返回列表就行
def read_csv_test(fname):
    with open(fname, 'r') as f:
        # 跳过文件头行 (列名)
        lines = f.readlines()[1:]
    tokens = [l.rstrip().split(',') for l in lines]
    return tokens
test_data = read_csv_test(os.path.join(data_dir, 'test.csv'))
print(test_data)

valid_ratio = 0.1
# reorg_train_valid(data_dir, labels, test_data, valid_ratio)

def copyfile(filename, target_dir):
    """将文件复制到目标目录。"""
    os.makedirs(target_dir, exist_ok=True)  # exist_ok：是否在目录存在时触发异常。如果exist_ok为False（默认值），
    # 则在目标目录已存在	的情况下触发FileExistsError异常；
    # 如果exist_ok为True，则在目标目录已存在的情况下不会触发FileExistsError异常。
    shutil.copy(filename, target_dir)  # 复制文件内容


# @save
def reorg_train_valid(data_dir, labels, test_data, valid_ratio):
    # 训练数据集中示例最少的类别中的示例数
    n = collections.Counter(labels.values()).most_common()[-1][1]  # [-1] 是最少的类别，如果[0]是最大的类别；
    # 最后的[1]则是返回值，如果是[0] 则返回个数
    # 验证集中每个类别的示例数
    n_valid_per_label = max(1, math.floor(n * valid_ratio))
    label_count = {}
    for train_file in os.listdir(os.path.join(data_dir, 'images')):
        fname = os.path.join(data_dir, 'images/', train_file)
        if ['images/' + train_file] in test_data:  # 如果图片地址在测试集的列表中
            copyfile(
                fname,
                os.path.join(data_dir, 'train_valid_test', 'test', 'unknown'))  # 将测试集也一一复制过来#测试集不知道标签，即为unknow
        else:  # if labels.__contains__('images/' + train_file)如果图片的地址在训练集的字典中
            label = labels['images/' + train_file]  # 取文件名，处理后的值作为labels的索引，即key值
            copyfile(
                fname,
                os.path.join(data_dir, 'train_valid_test', 'train_valid', label))  # 复制到train_valid中，
            if label not in label_count or label_count[label] < n_valid_per_label:
                copyfile(
                    fname,
                    os.path.join(data_dir, 'train_valid_test', 'valid', label))  # 复制到交叉验证集的文件中
                label_count[label] = label_count.get(label, 0) + 1  # 字典中get返回指定Key的值，如果key不存在则返回后面的参数，即0
            else:
                copyfile(
                    fname,
                    os.path.join(data_dir, 'train_valid_test', 'train', label))  # 复制到train中

    return n_valid_per_label





