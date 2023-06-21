import numpy as np
import cv2

from scipy.ndimage import map_coordinates



def geometric_transform_v1(image, rotation_angle, tx, ty, scale):
    theta = np.radians(rotation_angle)
    cos, sin = np.cos(theta), np.sin(theta)

    R = np.array([[cos, -sin],    # 旋转矩阵
                  [sin, cos]])
    S = np.array([[1/scale, 0],   # 缩放矩阵
                  [0, 1/scale]])
    T = np.array([-tx, -ty])      # 平移矩阵

    # 输出图像
    output = np.zeros_like(image)
    height, width = output.shape[:2]

    # 遍历输出图像中的每一个像素
    for y in range(height):
        for x in range(width):
            coord = np.array([y, x])
            inv_coord = ((S @ R) @ coord)
            inv_coord = np.round(inv_coord + T).astype(int) # 顺序应为缩放-旋转-平移
            # 检查坐标是否在输入图像内
            if 0 <= inv_coord[0] < height and 0 <= inv_coord[1] < width:
                # 在输入图像内的话则用双线性插值来获取像素值
                for c in range(output.shape[2]):
                    output[y, x, c] = map_coordinates(image[..., c], inv_coord[:, np.newaxis], order = 1)
    return output




def geometric_transform_v2(image, rotation_angle, tx, ty, scale):
    """
    @param image: 输入图像
    @param rotation_angle: 旋转角度，以度为单位
    @param tx, ty: 图像横轴与纵轴方向的平移量
    @param scale: 缩放因子
    """

    # 计算旋转角度的弧度值
    theta = np.radians(rotation_angle)
    cos, sin = np.cos(theta), np.sin(theta)
    R = np.array([[cos, -sin],      # 创建旋转矩阵
                  [sin, cos]])
    S = np.array([[scale, 0],       # 创建缩放矩阵
                  [0, scale]])
    T = np.array([tx, ty])          # 创建平移矩阵

    # 创建仿射变换矩阵
    A = np.hstack([S @ R, T.reshape(-1, 1)])
    A = np.vstack([A, [0, 0, 1]])   # 再为 cv2.warpAffine 函数添加最后一行

    # 应用仿射变换
    transformed_image = cv2.warpAffine(image, A[:2], (image.shape[1], image.shape[0]))

    return transformed_image


