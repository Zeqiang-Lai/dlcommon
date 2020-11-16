import torch
import matplotlib.pyplot as plt


def imshow_t(x):
    if type(x) == torch.Tensor:
        x = x.detach().cpu().numpy()
        x = x.transpose(1, 2, 0)
    plt.imshow(x)
    plt.show()
