import argparse
import os, sys, time, random, warnings


warnings.filterwarnings("ignore", category=UserWarning)



# 创建一个用于接收命令行参数对象
parser = argparse.ArgumentParser()

# 输入图像的路径
parser.add_argument('--input-image', type = str, 
            help = 'Accept the path of the input image')

# 直接设置通道个数，默认通道个数 3，如果读入图像
parser.add_argument('-c', '--channels',  type = int, default = 3, 
            help = 'Convert an image to grayscale or RGB')

# 四种噪声的添加，使用 0000-1111 编码设计，四个位置分别对应四种噪声 [高斯噪声, 椒盐噪声, 泊松噪声, 指数噪声]
parser.add_argument('-ns', '--noise',  type = str, default = '0000',
            help = 'Accept a mask represent four type of noise (gaussian, salt-and-pepper, Poisson or exponential noise). ')

# 调整输入图像的尺寸大小
parser.add_argument('-s', "--size", type = int, default = 224,
            help = 'Resize the input size of input image.')

# 下面是双边滤波器的参数，以下参数其实也有一部分能够泛化用于一般滤波器， i.e.作为通用性参数
parser.add_argument("--radius", type = int, default = 3, 
            help = 'Specified the kernel radius of the filter') 
parser.add_argument("--sigma-color", type = int, default = 10,
            help = 'Specified the sigma-color of the bilateral kernel')
parser.add_argument("--sigma-space", type = int, default = 10,
            help = 'Specified the sigma-space of the bilateral kernel')

# 下面是图像变化算法的参数，包括了旋转的角度、纵横方向平移的距离、以及缩放比率
parser.add_argument('--theta', type = int, default = 0,
            help = 'Specified the angle of the rotation')
parser.add_argument('--tx', type = int, default = 0,
            help = 'Specified the translation distance along the x-axis')
parser.add_argument('--ty', type = int, default = 0,
            help = 'Specified the translation distance along the y-axis')
parser.add_argument('--scale', type = float, default = 1,
            help = 'Specified the scale of the image')