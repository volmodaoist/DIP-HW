import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from processing.noise_maker import *
from processing.noise_filter import *


from ops.utils import *
from ops.config import *
from ops.measure import *

def compare_filters(args, images, filters, filters_param):
    results = []
    for img_name, img in images.items():
        for i, (filter_name, filter_func) in enumerate(filters.items()):
            noisy_img = masking_noise(img, noise_mask = args.noise)
            filtered_img = filter_func(noisy_img, *filters_param[i])

            result = {
                'Image': img_name,
                'Noise Mask': args.noise,
                'Filter': filter_name,
                'SSIM': ssim(img, filtered_img),
                'NMI': nmi(img, filtered_img),
                'CS': cs(img, filtered_img),
                'MSE': mse(img, filtered_img)
            }
            results.append(result)

    results = pd.DataFrame(results)
    results.to_csv('tmp.csv', index=False)
    return results


# python ./test/test_wiener_filter.py --size 224 --noise 1111
if __name__ == '__main__':
    args = parser.parse_args()

    images = { f"{i}.jpg" : read_image(f"{i}.jpg", resize_shape = args.size) for i in range(1, 6)}
    filters = {
        'Bilateral Filter': bilateral_filter_v2,
        'Wiener Filter': wiener_filter,
        'Guassian Filter': cv2.GaussianBlur
    }
    # 每个滤波器函数对应的参数
    filters_param = [
        [args.radius, args.sigma_color, args.sigma_space, args.step], 
        [], 
        [(3, 3), 0]
    ]
    

    print(compare_filters(args, images, filters, filters_param))
