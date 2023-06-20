from ops.utils import *
from ops.config import *

from processing.transform import *
from processing.noise_maker import *
from processing.noise_filter import *

# python main.py --input-image 1.jpg --size 224 --noise 1000
# python main.py --input-image 3.jpg --size 224 --scale 0.5
# python main.py --input-image 1.jpg --size 224 --theta 5 --scale 0.8
# python main.py --input-image 3.jpg --size 224 --tx 30 --ty 30 --theta 30
if __name__ == '__main__':
    args = parser.parse_args()
    img = read_image(args.input_image, resize_shape = args.size)
    t1 = geometric_transform_v1(img, args.theta, args.tx, args.ty, args.scale)
    t2 = geometric_transform_v2(img, args.theta, args.tx, args.ty, args.scale)
    plt.figure(figsize=(8, 6))
    plt.subplot(121)
    plt.imshow(t1)
    plt.subplot(122)
    plt.imshow(t2)    
    plt.savefig("tmp.png")
