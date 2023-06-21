import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

from ops.utils import *
from ops.config import *

from processing.transform import *

def lab_scalar(img):
    fig, axs = plt.subplots(3, 3, figsize = (15, 10))
    for i in range(1, 10):
        tmp = geometric_transform_v2(img, 0, 0, 0, 1 - 0.1 * i)
        row = (i - 1) // 3
        col = (i - 1) % 3
        axs[row, col].imshow(tmp)
        axs[row, col].set_title('Sclar: {:.1f}'.format(1 - 0.1 * i))

    # 删除 x 和 y 轴的刻度
    for ax in axs.ravel():
        ax.axis('off')
    plt.savefig("tmp.png")

# 运行下面单元测试查看单独旋转的效果
# python ./test/test_space_scalar.py --input-image 1.jpg --size 224 --noise 1000
# python ./test/test_space_scalar.py --input-image 3.jpg --size 224 --noise 1000
if __name__ == '__main__':
    args = parser.parse_args()
    img = read_image(args.input_image, resize_shape = args.size)
    lab_scalar(img)