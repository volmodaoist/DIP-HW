# 数字图像处理作业，代码开源

稍稍纪念一下本次图像处理的作业，本次作业是按照平时搭建科研流水线的方法来写的，

同时也希望能将数字图像处理之中学到的一些灵感用于模型鲁棒性提升上面…


# 使用方法
运行 `python main.py -h` 查看命令帮助

```
"""
optional arguments:
  --input-image INPUT_IMAGE
                        Accept the path of the input image
  
  -c CHANNELS, --channels CHANNELS
                        Convert an image to grayscale or RGB
  
  -ns NOISE, --noise NOISE
                        Accept a mask represent four type of noise (gaussian, salt-and-pepper, Poisson or exponential noise).
  
  -s SIZE, --size SIZE  
                        Resize the input size of input image.
  
  --radius RADIUS       
                        Specified the kernel radius of the filter
  
  --sigma-color SIGMA_COLOR
                        Specified the sigma-color of the bilateral kernel
  
  --sigma-space SIGMA_SPACE
                        Specified the sigma-space of the bilateral kernel
"""
```



**通过命令行的掩码参数添加对应噪声**

相较于先前的版本，现在我们能够通过 `--noise` 添加多种噪声，用户输入是一个四位二进制掩码，范围 `[0000, 1111]`，
四个位置分别对应高斯噪声、椒盐噪声、泊松噪声、指数噪声，其中数字零代表不添加对应类型的噪声，数字一代表添加对应类型的噪声

```shell
python ./noisy_processing/noise_maker.py --input-image 1.jpg --size 224 --noise 1000
python ./noisy_processing/noise_maker.py --input-image 1.jpg --size 224 --noise 1111
```



**命令行执行下列命令即可查看双边滤波对于不同参数的影响**

```shell
python main.py --filename 1.jpg -n gaussian --lab hyper-grid --size 100
python main.py --filename 1.jpg -n gaussian --lab hyper-diam --size 100
python main.py --filename 1.jpg -n gaussian --lab hyper-step --size 100
```

上述命令分别探究以下三种超参数：

- 空域与色域构成的笛卡尔积对于去噪效果的影响
- 滤波器的半径对于去噪效果的硬性
- 滤波器的步长对于去噪效果的影响


接下来我们需要明确的事情
- 如何修改命令行参数文件 (命令行参数控制需要重新设计)
- 需要解决如何添加噪声、如何度量图像质量等等、图像旋转角度、颜色空间的变化
- 二维的维纳滤波器怎么实现
- 如何使用傅里叶变化嵌入水印，如何实现傅里叶变化