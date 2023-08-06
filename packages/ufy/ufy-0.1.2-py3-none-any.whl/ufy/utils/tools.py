import os

from PIL import Image
import numpy as np
from scipy import ndimage as ndi
import cv2


def energy(img, savename='energy.jpg', issave=False):
    """
        Simple gradient magnitude energy map.
    """
    xgrad = ndi.convolve1d(img, np.array([1, 0, -1]), axis=1, mode='wrap')
    ygrad = ndi.convolve1d(img, np.array([1, 0, -1]), axis=0, mode='wrap')

    grad_mag = np.sqrt(np.sum(xgrad ** 2, axis=2) + np.sum(ygrad ** 2, axis=2))

    if issave:
        # cv2.imwrite(savename, grad_mag.astype(np.uint8))
        image = Image.fromarray(grad_mag.astype(np.uint8))
        image.save(savename)
    return grad_mag


def find_file(dir_source,file_format=[['mrxs', 'tiff', 'npdi']],file_list=[]):

    dirlist = os.listdir(dir_source)

    for f in dirlist:
        f = os.path.join(dir_source,f)
        if os.path.isdir(f):
            find_file(f,file_format,file_list)
        elif str.lower(os.path.basename(f).split('.')[-1]) in file_format:
            file_list.append(f)

if __name__ == '__main__':
    alllist = []
    find_file("E:/OneDrive/rebar/一期善后/stitich",file_format=['bmp','jpg'],file_list=alllist)
    print(alllist)
