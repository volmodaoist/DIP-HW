import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from processing.noise_maker import *
from processing.noise_filter import *


from ops.utils import *
from ops.config import *
from ops.measure import *

def lab_bilateral_filter_grid(image, noisy_img, sigma_colors, sigma_spaces):
    # 创建子图矩阵
    fig, axs = plt.subplots(len(sigma_colors), len(sigma_spaces), figsize = (10, 10))
    # 遍历 sigma_colors 和 sigma_spaces
    ssim_list, nmi_list, cs_list, mse_list = [], [], [], []
    for i in range(len(sigma_colors)):
        for j in range(len(sigma_spaces)):
            # 使用当前的sigma_color和sigma_space进行双边滤波
            filtered_img = bilateral_filter_v2(noisy_img, 3, sigma_colors[i], sigma_spaces[j])
            # 在子图矩阵中展示结果
            axs[i, j].imshow(filtered_img, aspect = 'equal')
            axs[i, j].axis('off')
            axs[i, j].set_title(f"sigma_color={sigma_colors[i]}, sigma_space={sigma_spaces[j]}")
            ssim_list.append(ssim(image, filtered_img))
            nmi_list.append(nmi(image, filtered_img))
            cs_list.append(cs(image, filtered_img))
            mse_list.append(mse(image, filtered_img))
    df = pd.DataFrame({'sigma_color': sigma_colors * len(sigma_spaces), 'sigma_space': sigma_spaces * len(sigma_colors), 'ssim': ssim_list, 'nmi': nmi_list, 'cs': cs_list, 'mse': mse_list})
    plt.savefig("tmp.png")
    print(df)


# 运行下面代码获取测试表格
# python ./test/test_bilateral_filter_grid.py --input-image 1.jpg --size 224 --noise 1000 
if __name__ == "__main__":
    args = parser.parse_args()

    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)
    filtered_img = bilateral_filter_v2(image = noisy_img, 
                                    radius = args.radius, 
                                    sigma_color = args.sigma_color, 
                                    sigma_space = args.sigma_space)

    lab_bilateral_filter_grid(img, noisy_img, sigma_colors = [10, 20, 30], sigma_spaces = [10, 20, 30])
