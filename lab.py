from Args import *
from utils import *
from measure import *
from noise_maker import *
from noise_filter import *

def lab_runing_time(noisy_img):
    # 函数运行时间测试器
    print("Total Running Time: {:.3f}s!".format(func_counter(bilateral_filter_v1, func_args = [noisy_img, 3, 10, 10])))
    print("Total Running Time: {:.3f}s!".format(func_counter(bilateral_filter_v2, func_args = [noisy_img, 3, 10, 10])))


def lab_compare_images(image, noisy_img, filtered_img):
    # 展示图像
    plt.figure(figsize = (6, 6))
    plt.subplot(131)
    plt.title("Original")
    plt.imshow(image.astype(np.uint8), aspect = 'equal')
    plt.axis("off")
    plt.subplot(132)
    plt.title("Noisy")
    plt.imshow(noisy_img.astype(np.uint8), aspect = 'equal')
    plt.axis("off")
    plt.subplot(133)
    plt.title("Filtered")
    plt.imshow(filtered_img.astype(np.uint8), aspect = 'equal')
    plt.axis("off")
    plt.show()


def lab_bilateral_filter_grid(image, noisy_img, sigma_colors, sigma_spaces):
    # 创建子图矩阵
    fig, axs = plt.subplots(len(sigma_colors), len(sigma_spaces), figsize=(10, 10))
    # 遍历sigma_colors和sigma_spaces
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
    plt.show()
    df = pd.DataFrame({'sigma_color': sigma_colors * len(sigma_spaces), 'sigma_space': sigma_spaces * len(sigma_colors), 'ssim': ssim_list, 'nmi': nmi_list, 'cs': cs_list, 'mse': mse_list})
    print(df)


def lab_bilateral_filter_step(image, noisy_img, step_sizes):
    # 创建子图矩阵
    fig, axs = plt.subplots(1, len(step_sizes), figsize=(10, 10))
    # 遍历sigma_colors和sigma_spaces
    ssim_list, nmi_list, cs_list, mse_list = [], [], [], []
    for k in range(len(step_sizes)):
        # 使用当前的sigma_color、sigma_space和step_size进行双边滤波
        filtered_img = bilateral_filter_v2(noisy_img, step_sizes[k], 30, 30)
        # 在子图矩阵中展示结果
        axs[k].imshow(filtered_img, aspect = 'equal')
        axs[k].axis('off')
        axs[k].set_title(f"step_size={step_sizes[k]}")
        ssim_list.append(ssim(image, filtered_img))
        nmi_list.append(nmi(image, filtered_img))
        cs_list.append(cs(image, filtered_img))
        mse_list.append(mse(image, filtered_img))
    plt.show()
    df = pd.DataFrame({'step_size': step_sizes, 'ssim': ssim_list, 'nmi': nmi_list, 'cs': cs_list, 'mse': mse_list})
    print(df)


def lab_bilateral_filter_diameter(image, noisy_img, diam_sizes):
    # 创建子图矩阵
    fig, axs = plt.subplots(1, len(diam_sizes), figsize=(10, 10))
    # 遍历sigma_colors和sigma_spaces
    ssim_list, nmi_list, cs_list, mse_list = [], [], [], []
    for k in range(len(diam_sizes)):
        # 使用当前的sigma_color、sigma_space和step_size进行双边滤波
        filtered_img = bilateral_filter_v2(noisy_img, diam_sizes[k], 30, 30, step = 1)
        # 在子图矩阵中展示结果
        axs[k].imshow(filtered_img, aspect = 'equal')
        axs[k].axis('off')
        axs[k].set_title(f"diam_size={diam_sizes[k]}")
        ssim_list.append(ssim(image, filtered_img))
        nmi_list.append(nmi(image, filtered_img))
        cs_list.append(cs(image, filtered_img))
        mse_list.append(mse(image, filtered_img))
    plt.show()
    df = pd.DataFrame({'diam_size': diam_sizes, 'ssim': ssim_list, 'nmi': nmi_list, 'cs': cs_list, 'mse': mse_list})
    print(df)


## 下面的内容是一个扩展的实验

import torch
import torchvision.transforms as transforms

from PIL import Image
from torch.autograd import Variable
from torchvision.models import resnet18
def lab_classify_resnet(img, model = resnet18(pretrained = True), transform = transforms.Compose([transforms.Resize((224, 224)),transforms.ToTensor()])):
    def classify(x, model):
        with torch.no_grad():
            output = model(x)                         # 使用模型进行分类
            prob = torch.softmax(output, dim=1)       # 对输出进行 softmax 处理
            _, predicted = torch.max(prob.data, 1)    # 获取分类结果
        return predicted

    img = Image.fromarray(img.astype('uint8'))
    img = transform(img)                          # 预处理图像
    img = img.unsqueeze(0)

    # 例如图片 5 正确类别Tench，对应的 label 0，下面开始尝试对其进行对抗攻击
    model.eval()
    predicted = classify(img, model)
    print("Clean prediction: ", predicted.item())

    epsilon = 0.01
    x_adv = Variable(img.data, requires_grad=True)
    loss = torch.nn.functional.cross_entropy(model(x_adv), predicted)
    loss.backward()
    x_adv = x_adv + epsilon * torch.sign(x_adv.grad)
    x_adv = torch.clamp(x_adv, 0, 1)
    
    # 对生成的对抗样本进行预测
    predicted_adv = classify(x_adv, model)
    print("Adversarial prediction: ", predicted_adv.item())


    # 去噪然后再次预测
    x_adv_np = x_adv.squeeze().permute(1, 2, 0).detach().cpu().numpy() * 255
    x_adv_np = x_adv_np.astype("float32")
    filtered_img = bilateral_filter_v2(x_adv_np, 1, 75, 75, step = 1)
    filtered_img = Image.fromarray(filtered_img)
    filtered_img = transform(filtered_img)                          # 预处理图像
    filtered_img = filtered_img.unsqueeze(0)
    model.eval()
    predicted = classify(filtered_img, model)
    print("Filtered prediction: ", predicted_adv.item())



    
