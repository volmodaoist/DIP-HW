# 数字图像处理作业，代码开源

稍稍纪念一下本次图像处理的作业，本次作业是按照平时搭建科研流水线的方法来写的，

同时也希望能将数字图像处理之中学到的一些灵感用于模型鲁棒性提升上面…


# 使用方法
运行 `python main.py -h` 查看命令帮助

```
"""
optional arguments:
  -h, --help            show this help message and exit
  
  -f FILENAME, --filename FILENAME
                        input file name
  -c {gray,rgb}, --channels {gray,rgb}
                        convert image to grayscale or RGB

  -n {gaussian,salt-and-pepper,poisson,exponential}, 
  --noise {gaussian,salt-and-pepper,poisson,exponential}
                        mask Gaussian, salt-and-pepper, Poisson or exponential noise
                        
  -l {running-time,compare,hyper-grid,hyper-step,hyper-diam,attack}, 
  --lab {running-time,compare,hyper-grid,hyper-step,hyper-diam,attack}
                        decide which experiment to run
                        
  -s SIZE, --size SIZE  set image size
"""
```



**命令行执行下列命令即可查看双边滤波对于不同噪声去噪效果**

```shell
python main.py --filename 4.jpg --noise salt-and-pepper
python main.py --filename 4.jpg --noise exponential
python main.py --filename 4.jpg --noise poisson
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