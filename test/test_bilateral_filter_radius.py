
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from processing.noise_maker import *
from processing.noise_filter import *


from ops.utils import *
from ops.config import *
from ops.measure import *

def lab_bilateral_filter_radius(image, noisy_img, radius_sizes):
    # 创建子图矩阵
    fig, axs = plt.subplots(1, len(radius_sizes), figsize=(10, 10))
    # 遍历sigma_colors和sigma_spaces
    ssim_list, nmi_list, cs_list, mse_list = [], [], [], []
    for k in range(len(radius_sizes)):
        # 使用当前的sigma_color、sigma_space和step_size进行双边滤波
        filtered_img = bilateral_filter_v2(noisy_img, radius_sizes[k], 30, 30, step = 1)
        # 在子图矩阵中展示结果
        axs[k].imshow(filtered_img, aspect = 'equal')
        axs[k].axis('off')
        axs[k].set_title(f"diam_size={radius_sizes[k]}")
        ssim_list.append(ssim(image, filtered_img))
        nmi_list.append(nmi(image, filtered_img))
        cs_list.append(cs(image, filtered_img))
        mse_list.append(mse(image, filtered_img))
    df = pd.DataFrame({'radius_size': radius_sizes, 'ssim': ssim_list, 'nmi': nmi_list, 'cs': cs_list, 'mse': mse_list})
    plt.savefig("tmp.png")
    print(df)


# 运行下面代码获取测试表格
# python ./test/test_bilateral_filter_radius.py --input-image 1.jpg --size 224 --noise 1000 
if __name__ == "__main__":
    args = parser.parse_args()

    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)
    filtered_img = bilateral_filter_v2(image = noisy_img, 
                                    radius = args.radius, 
                                    sigma_color = args.sigma_color, 
                                    sigma_space = args.sigma_space)

    lab_bilateral_filter_radius(img, noisy_img, radius_sizes = [1,3,5,7,9])



