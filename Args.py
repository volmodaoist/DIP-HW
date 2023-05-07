import argparse
class MyArgs():
    def __init__(self):
        self.parser = argparse.ArgumentParser()  # create an ArgumentParser object
        self.parser.add_argument('-f', '--filename', 
                    type = str, 
                    help = 'input file name')
        self.parser.add_argument('-c', '--channels', 
                    choices = ['gray', 'rgb'], 
                    default = 'rgb',
                    help = 'convert image to grayscale or RGB')
        self.parser.add_argument('-n', '--noise', 
                    choices = ['gaussian', 'salt-and-pepper', 'poisson', 'exponential'],  
                    default = 'gaussian',
                    help = 'mask Gaussian, salt-and-pepper, Poisson or exponential noise')
        self.parser.add_argument("-l", "--lab",
                    choices = ['running-time', 'compare', 'hyper-grid', 'hyper-step', 'hyper-diam', 'attack'],
                    default = 'compare',
                    help = 'decide which experiment to run')
        self.parser.add_argument("-s", "--size",
                    type = int,
                    default = None,
                    help = 'set image size')
    def parse_args(self):
        return vars(self.parser.parse_args())
