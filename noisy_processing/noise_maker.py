import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))


from ops.utils import *
from ops.config import *

# 所有涉及加减法的噪声运算都应添加 clip 控制图像的范围

def masking_gaussian_noise(img, mean = 0, std = 15):
    noise = np.random.normal(mean, std, img.shape)
    # 早期此处返回值 np.uint8 是一切不幸的根源
    return np.clip(img + noise, 0, 255).astype(np.uint16)

def masking_salt_and_pepper_noise(img, prob=0.01):
    h, w, c = img.shape
    rdn = np.random.rand(h, w, c)
    thres = 1 - prob
    noisy_image = np.zeros((h, w, c), dtype = np.uint16)
    
    # 使用概率矩阵的方法实现向量化运算，通过条件表达式进行赋值，
    # 如果随机数小于 prob，设为 0，如果随机数大于 1-prob，设为 255，否则，使用原图像的数值，
    # 也即区间两侧设为极端值，中间保留原图的数值！
    noisy_image[rdn < prob] = 0
    noisy_image[rdn > thres] = 255
    noisy_image[(rdn >= prob) & (rdn <= thres)] = img[(rdn >= prob) & (rdn <= thres)]
    
    return noisy_image

# 泊松噪声是一种常见的信号或图像噪声，是信号强度的函数，如果图像强度不高，或说如果图像的动态范围 i.e.像素值的最大值和最小值之差较小，
# 那么添加的噪声可能在视觉上不太明显那么泊松噪声不怎么明显
def masking_poisson_noise(img):
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy_image = np.random.poisson(img * vals) / float(vals)
    return np.clip(noisy_image, 0, 255).astype(np.uint16)

def masking_exponential_noise(img, scale = 1.0):
    noisy = np.random.exponential(scale, img.shape)
    noisy = noisy / np.max(noisy) * 255
    return np.clip(img + noisy, 0, 255).astype(np.int16)


def masking_noise(img, noise_mask):
    if not all(bit in '01' for bit in noise_mask):
        raise ValueError("Invalid mask. Mask should be a 4-digit binary string representing ['gaussian', 'salt-and-pepper', 'poisson', 'exponential']")
    if noise_mask[0] == '1':
        img = masking_gaussian_noise(img)
    if noise_mask[1] == '1':
        img = masking_salt_and_pepper_noise(img)
    if noise_mask[2] == '1':
        img = masking_poisson_noise(img)
    if noise_mask[3] == '1':
        img = masking_exponential_noise(img)
    return img.astype(np.uint16)


# 此为单元测试，导入这个 py 文件的时候，main 上下文之中的内容将被忽略, 运行下列模块的时候要求保持 main.py 文件同级目录
# 相较于先前的版本，本次噪声采用了掩码开关机制实现，允许叠加多种噪声

# python ./noisy_processing/noise_maker.py --input-image 1.jpg --size 224 --noise 1000
# python ./noisy_processing/noise_maker.py --input-image 1.jpg --size 224 --noise 1111

if __name__ == '__main__':
    args = parser.parse_args()
    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)

    plt.figure(figsize = (8, 6))
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(img, aspect = 'equal')

    plt.subplot(122)
    plt.title("Noisy")
    plt.imshow(noisy_img, aspect = 'equal')

    plt.savefig("tmp.png")
    plt.show()