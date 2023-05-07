from utils import *

def masking_gaussian_noise(img, mean = 0, std = 15):
    h, w, c = img.shape
    noise = np.random.normal(mean, std, (h, w, c))
    # 此处返回值 np.uint8 是一切不幸的根源
    return np.clip(img + noise, 0, 255)

def masking_salt_and_pepper_noise(img, prob=0.01):
    h, w, c = img.shape
    noise = np.zeros((h, w, c), dtype=np.uint8)
    thres = 1 - prob
    for i in range(h):
        for j in range(w):
            rdn = np.random.rand()
            if rdn < prob:
                noise[i][j] = 0
            elif rdn > thres:
                noise[i][j] = 255
            else:
                noise[i][j] = img[i][j]
    return noise

def masking_poisson_noise(img):
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy = np.random.poisson(img * vals) / float(vals)
    return noisy

def masking_exponential_noise(img, scale = 1.0):
    noisy = np.random.exponential(scale, img.shape)
    noisy = noisy / np.max(noisy) * 255
    return np.clip(img + noisy, 0, 255)



def masking_noise(img, noise_type):
    if noise_type == 'gaussian':
        return masking_gaussian_noise(img)
    elif noise_type == 'salt-and-pepper':
        return masking_salt_and_pepper_noise(img)
    elif noise_type == 'poisson':
        return masking_poisson_noise(img)
    elif noise_type == 'exponential':
        return masking_exponential_noise(img)
    else:
        raise ValueError("Invalid noise type. Choose from 'gaussian', 'salt-and-pepper', 'poisson', 'exponential'.")

