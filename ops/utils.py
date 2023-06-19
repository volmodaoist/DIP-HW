import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os, sys, cv2, time, random, torch


"""
这个模块里面自定义了一些实用工具函数，其中读入图片会被 resize 设为 224 x 224，
这个尺寸是按 ImageNet 常用训练规格设计的 ^_^
"""

# 随机数种子设置函数
def seed_everthing(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True


# 图像读入函数
def read_image(filename, resize_shape = None, default_path = "./test_images/"):
    img = cv2.imread(default_path + filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if resize_shape is not None and isinstance(resize_shape, tuple):
        img = cv2.resize(img, dsize = resize_shape, interpolation = cv2.INTER_LINEAR)
    elif isinstance(resize_shape, int):
            img = cv2.resize(img, dsize = (resize_shape, resize_shape), interpolation = cv2.INTER_LINEAR)
    else:
        if len(img.shape) == 2:
            img = img[:, :, np.newaxis]
        H, W, C = img.shape
        img = cv2.resize(img, dsize = (H//2, W//2), interpolation = cv2.INTER_LINEAR)
    return img.astype(np.int16)


# 函数计时器
def func_counter(func, func_args):
    start_time = time.time()
    func(*func_args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time
