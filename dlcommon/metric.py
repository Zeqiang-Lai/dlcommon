import torch


def PSNR(x, gt, data_range=1):
    mse = torch.mean((x - gt) ** 2)
    return 10 * torch.log10(data_range ** 2 / mse)
