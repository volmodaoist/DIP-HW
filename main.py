from Args import *
from lab import *
from utils import *
from noise_maker import *
from noise_filter import *


args = MyArgs().parse_args()

# python main.py --filename 4.jpg --noise gaussian
# python main.py --filename 4.jpg --noise salt-and-pepper
# python main.py --filename 4.jpg --noise poisson
# python main.py --filename 4.jpg --noise exponential

if __name__ == '__main__':
    # 读取原始图片
    img = read_image(args["filename"], resize_shape = args["size"])
    # 添加噪声
    noisy_img = masking_noise(img, noise_type = args['noise'])
    # 双边滤波去噪
    filtered_img = bilateral_filter_v2(noisy_img, 3, 10, 10)

    # 运行不同的实验
    if args['lab'] == 'running-time':
        lab_runing_time(noisy_img)
    elif args['lab'] == 'compare':
        lab_compare_images(img, noisy_img, filtered_img)
    elif args['lab'] == 'hyper-grid':
        lab_bilateral_filter_grid(img, noisy_img, sigma_colors = [10, 20, 30], sigma_spaces = [10, 20, 30])
    elif args['lab'] == 'hyper-step':
        lab_bilateral_filter_step(img, noisy_img, step_sizes = [1,3,5,7,9])
    elif args['lab'] == 'hyper-diam':
        # 其实严格来说这里测量的是一个半径，但是取名的时候写成了直径...
        lab_bilateral_filter_diameter(img, noisy_img, diam_sizes = [1,3,5,7,9])
    elif args['lab'] == 'attack':
        lab_classify_resnet(img)
