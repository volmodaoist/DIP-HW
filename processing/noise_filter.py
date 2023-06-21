import os, sys, cv2
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from scipy.signal import convolve2d
from processing.noise_maker import *

from ops.utils import *
from ops.config import *




# 双边滤波基础版，程序运行时间: 29.69884419441223s
def bilateral_filter_v1(image, radius, sigma_color, sigma_space):
    image = image.astype(float)
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
    H, W, C = image.shape
    output_image = image.copy()
    for i in range(radius, H - radius):
        for j in range(radius, W - radius):
            for k in range(C):
                weight_sum, pixel_sum = 0, 0
                for x in range(-radius, radius + 1):
                    for y in range(-radius, radius + 1):
                        spatial_weight = -(x ** 2 + y ** 2) / (2 * (sigma_space ** 2))                                  # 空间域权重
                        color_weight = -(image[i][j][k] - image[i + x][j + y][k]) ** 2 / (2 * (sigma_color ** 2))       # 颜色域权重
                        """
                        OpenCV 读入图像，默认转为 uint8 类型的数组，强烈建议转为 int16，本人近乎六个小时 debug 都花在了这个地方
                        使用 uint8 类型的 numpy 数组进行数值计算时会自动进行溢出截断，即超出取值范围的数值会被截断为取值范围内的数值，
                        因此减法结果可能是截断后的正数而非负数，导致计算的结果出错，影响后序 np.exp 计算，最终生成的图像会变得非常模糊！
                        """
                        weight = np.exp(spatial_weight + color_weight)      # 像素整体权重
                        weight_sum += weight                                # 求权重和，用于归一化
                        pixel_sum += (weight * image[i + x][j + y][k])
                
                value = pixel_sum / weight_sum
                output_image[i][j][k] = value                               # 归一化后的像素值
    return output_image.astype(np.uint16)


# 双边滤波向量版，程序运行时间: 3.4048819541931152s
def bilateral_filter_v2(image, radius = 3, sigma_color = 10, sigma_space = 10, step = 1):
    image = image.astype(float)
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
    H, W, C = image.shape
    diameter = radius * 2 + 1
    space_kernel = np.zeros((diameter, diameter))
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
                space_kernel[x + radius, y + radius] = -(x ** 2 + y ** 2) / (2 * (sigma_space ** 2))
    output_image = image.copy()
    for i in range(radius, H - radius, step):
        for j in range(radius, W - radius, step):
            for k in range(C):
                image_kernel = image[i - radius : i + radius + 1, j - radius: j + radius + 1, k]
                color_kernel = - (image[i][j][k]  - image_kernel) ** 2 /  (2 * (sigma_color ** 2)) 
                weights = np.exp(space_kernel + color_kernel)
                weights_sum = weights.sum()
                pixel_sum = (weights * image_kernel).sum()
                value = pixel_sum / weights_sum
                output_image[i][j][k] = value
    return output_image.astype(np.uint16)



def estimate_noise(image, box_size = 5):
    """
    Estimate the noise variance from an image.
    @param image:   The input image
    @param box_size: Size of the box to compute local variance
    """
    image = image.astype(float)  # 将 image 转换为 float 类型
    mean = cv2.blur(image, (box_size, box_size))
    variance = cv2.blur(image**2, (box_size, box_size)) - mean**2

    # 选取局部方差的前 10% 作为噪声方差的估计值，使用 np.percentile() 函数来实现。
    var_top10 = variance[variance < np.percentile(variance, 10)]
    return np.mean(var_top10) if np.size(var_top10) != 0 else 0


def wiener_filter_channel(img, kernel, noise_var):
    """
    Apply a Wiener filter to a single channel of the input image.

    @param img:    Input image
    @param kernel: Filter kernel
    @param noise_var: The noise variance
    """
    kernel /= np.sum(kernel)
    
    pad_width = kernel.shape[0] // 2                        # 算出需要填充的边缘圈数
    img_padded = np.pad(img, pad_width, mode = 'edge')      # 填充图像
    dummy = convolve2d(img_padded, kernel, mode = 'valid')  # 使用卷积核

    sigma = np.sum((dummy - img)**2) / float(dummy.size)

    noise_var = noise_var / float(sigma)

    if noise_var < 0.0:
        noise_var = sigma

    result = dummy - noise_var / (img + noise_var +  1e-10) * dummy
    
    return np.clip(result, 0, 255).astype(np.uint16)

def wiener_filter(image):
    # 输入一张图像，将其转为 float32 类型进行运算，返回的时候再转为 uint16
    image = np.float32(image)
    kernel = np.ones((3,3)) / 9
    noise_var = estimate_noise(image)

    # 对每个通道单独滤波
    filtered_image = np.zeros_like(image)
    if len(image.shape) == 3 and image.shape[-1] == 3: 
        for i in range(3):
            filtered_image[:, :, i] = wiener_filter_channel(image[:, :, i], kernel, noise_var)
    elif image.shape[-1] == 1:
        filtered_image = wiener_filter_channel(image, kernel, noise_var)
    else:
        raise ValueError("Dimension should be one(Gray) or three(RGB)!")

    return filtered_image.astype(np.uint16)





# 此为单元测试，运行下面的代码将会看到滤波的效果，并且给出原图、噪声图、滤波图之间的对比
# python ./processing/noise_filter.py --input-image 1.jpg --size 224 --noise 1000 --radius 3 --sigma-color 10 --sigma-space 10
# python ./processing/noise_filter.py --input-image 1.jpg --size 224 --noise 1111 --radius 3 --sigma-color 10 --sigma-space 10
if __name__ == "__main__":
    args = parser.parse_args()
    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)
    b_filtered_img = bilateral_filter_v2(image = noisy_img, 
                                     radius = args.radius, 
                                     sigma_color = args.sigma_color, 
                                     sigma_space = args.sigma_space)
    w_filtered_img = wiener_filter(img)

    image_list = [img, noisy_img, b_filtered_img, w_filtered_img]
    image_title = ["Original", "Noisy", "Bilateral Filter", "Wiener Filter"]
    plt.figure(figsize=(8, 6))
    for i, (image, title) in enumerate(zip(image_list, image_title)):
        plt.subplot(1, 4, i + 1)
        plt.title(title)
        plt.imshow(image, aspect='equal')
        plt.axis('off')
    plt.savefig("tmp.png")

