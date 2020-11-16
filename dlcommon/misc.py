import numpy as np


def scale_to_01(x):
    maxn = np.max(x)
    minn = np.min(x)
    return (x - minn) / (maxn - minn)


def scale_01_to_255(x):
    x = np.clip(x, 0, 1) * 255
    return x.astype(np.uint8)


def img2patch(img, win, stride=5, channel_first=False):
    """
    Convert image into patches

    :param img: [W, H, C] or [C, W, H] with channel_first=True
    :param win: square patch size
    :return: a list of patches
    """
    if channel_first:
        img = img.transpose(1, 2, 0)
    patches = []
    w, h = img.shape[0], img.shape[1]
    i, j = 0, 0
    while i + win < w:
        while j + win < h:
            patch = img[i:i + win, j:j + win, :]
            if channel_first:
                patch = patch.transpose(2, 0, 1)
            patches.append(patch)
            j += stride
        i += stride
        j = 0
    return patches
