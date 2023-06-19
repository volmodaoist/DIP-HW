from ops.config import *
from ops.utils import *

from noisy_processing.noise_maker import *
from noisy_processing.noise_filter import *

def ssim(image1, image2):
    # 使用numpy实现ssim
    mu1 = np.mean(image1)
    mu2 = np.mean(image2)
    sigma1 = np.var(image1)
    sigma2 = np.var(image2)
    sigma12 = np.cov(image1.flatten(), image2.flatten())[0][1]
    k1, k2, L = 0.01, 0.03, 255
    C1, C2 = (k1 * L) ** 2, (k2 * L) ** 2
    l12 = (2 * mu1 * mu2 + C1) / (mu1 ** 2 + mu2 ** 2 + C1)
    c12 = (2 * np.sqrt(sigma1) * np.sqrt(sigma2) + C2) / (sigma1 + sigma2 + C2)
    C3 = C2 / 2
    s12 = (sigma12 + C3) / (np.sqrt(sigma1) * np.sqrt(sigma2) + C3)
    return l12 * c12 * s12
    
def nmi(image1, image2):
    # 计算两张图片的互信息，要避免分母除以零的情况
    hgram, x_edges, y_edges = np.histogram2d(image1.ravel(), image2.ravel(), bins=256)
    pxy = hgram / float(np.sum(hgram))
    px = np.sum(pxy, axis=1)
    py = np.sum(pxy, axis=0)
    px_py = px[:, None] * py[None, :]
    nzs = pxy > 0
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))

def cs(image1, image2):
    # 使用numpy实现cs
    return np.dot(image1.flatten(), image2.flatten()) / (np.linalg.norm(image1) * np.linalg.norm(image2))

def mse(image1, image2):
    # 使用numpy实现mse
    return np.mean((image1 - image2) ** 2)