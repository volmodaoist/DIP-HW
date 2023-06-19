from ops.utils import *
from ops.config import *
from noisy_processing.noise_maker import *
from noisy_processing.noise_filter import *


# python main.py --input-image 1.jpg --size 224 
# python main.py --input-image 1.jpg --size 224 --noise 1000
if __name__ == '__main__':
    args = parser.parse_args()
    
    img = read_image(args.input_image, resize_shape = args.size)
    noisy_img = masking_noise(img, noise_mask = args.noise)
    filtered_img = bilateral_filter_v2(image = noisy_img, 
                                    radius = args.radius, 
                                    sigma_color = args.sigma_color, 
                                    sigma_space = args.sigma_space)
