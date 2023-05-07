from utils import *

# 程序运行时间: 29.69884419441223s
def bilateral_filter_v1(image, radius, sigma_color, sigma_space):
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
    return output_image.astype(np.uint8)


# 程序运行时间: 3.4048819541931152s
def bilateral_filter_v2(image, radius, sigma_color, sigma_space, step = 1):
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
    return output_image.astype(np.uint8)