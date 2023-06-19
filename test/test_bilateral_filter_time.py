import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from noisy_processing.noise_maker import *
from noisy_processing.noise_filter import *

from ops.utils import *
from ops.config import *

# 运行时间对比：如果使用整数类型，运算期间有可能出现溢出，故在运行期间要先转为 flaot 类型
# python ./test/test_bilateral_filter_time.py --input-image 1.jpg --size 224 --noise 1000 --radius 3 --sigma-color 10 --sigma-space 10

if __name__ == "__main__":    
    args = parser.parse_args()
    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)

    print("Total Running Time: {:.3f}s!".format(func_counter(bilateral_filter_v1, func_args = [noisy_img, args.radius, args.sigma_color, args.sigma_space])))
    print("Total Running Time: {:.3f}s!".format(func_counter(bilateral_filter_v2, func_args = [noisy_img, args.radius, args.sigma_color, args.sigma_space])))
