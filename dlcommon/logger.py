import os

import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import logging
import time
import sys

class TextLogger(object):
    def __init__(self, rank, save):
        self.rank = rank
        if self.rank == 0:
            log_format = '%(asctime)s %(message)s'
            logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                                format=log_format, datefmt='%m/%d %I:%M:%S %p')
            fh = logging.FileHandler(os.path.join(save, 'log.txt'))
            fh.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(fh)
            self.start_time = time.time()

    def info(self, string, *args):
        if self.rank == 0:
            elapsed_time = time.time() - self.start_time
            elapsed_time = time.strftime(
                '(Elapsed: %H:%M:%S) ', time.gmtime(elapsed_time))
            if isinstance(string, str):
                string = elapsed_time + string
            else:
                logging.info(elapsed_time)
            logging.info(string, *args)


class TensorboardLogger:
    def __init__(self, log_dir=None, global_step=0):
        self.global_step = global_step

        if not log_dir:
            import socket
            from datetime import datetime
            current_time = datetime.now().strftime('%b%d_%H-%M-%S')
            log_dir = os.path.join('runs' + current_time + '_' + socket.gethostname())

        self.log_dir = log_dir
        self.writer = SummaryWriter(log_dir=self.log_dir)

    def step(self, count=1):
        self.global_step += count

    def reset(self):
        self.global_step = 0

    def add_scalar(self, tag, value):
        if type(value) == torch.Tensor:
            value = value.item()
        self.writer.add_scalar(tag, value, self.global_step)

    def add_image(self, tag, img):
        self.writer.add_image(tag, img, self.global_step)

    def add_grid_images(self, tag, images: list):
        grid = torchvision.utils.make_grid(images)
        self.writer.add_image(tag, grid, self.global_step)

    def close(self):
        self.writer.close()

    def state_dict(self):
        return {'global_step': self.global_step, 'log_dir': self.log_dir}

    @staticmethod
    def load_state_dict(state_dict):
        return TensorboardLogger(log_dir=state_dict['log_dir'],
                                 global_step=state_dict['global_step'])