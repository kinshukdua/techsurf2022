from typing import Tuple
from skimage import img_as_float
import PIL.Image
from skimage.metrics import structural_similarity as ssim
import multiprocessing
import torch
from models import model

def test_compression(img: PIL.Image, ratio: float) -> Tuple[float, float]:
    """
    A function to test the compression ratio of an image.
    Returns the structural similarity index and the ratio.
    Arguments:
        img: PIL.Image
        ratio: float
    Returns:
        ratio: float
        ssim: float
    """
    height = img.size[0]
    width = img.size[1]
    img_compressed = img.resize((int(height*ratio), int(width*ratio)), PIL.Image.LANCZOS)
    img_compressed = img_compressed.resize((height, width),PIL.Image.LANCZOS)
    img = img_as_float(img)
    img_compressed = img_as_float(img_compressed)
    return (ratio, ssim(img, img_compressed,  
            data_range=img_compressed.max() - img_compressed.min(),
            channel_axis=2))


def optimal_compression(img) -> int:
    """
    A function to find the optimal compression ratio of an image.
    Returns the optimal ratio and the compressed image.
    Arguments:
        img: PIL.Image
    Returns:
        ratio: float
        image: compressed image
    """
    image = PIL.Image.open(img)
    # hard coded ratio
    # ratios = [(image.copy(), i) for i in (0.1, 0.25, 0.33, 0.4, 0.5, 0.6, 0.75, 1)]
    # better approach
    num_of_cores = multiprocessing.cpu_count()
    ratios = [(image.copy(),i/num_of_cores) for i in range(1, num_of_cores)]
    pool = multiprocessing.Pool(8)
    print("Processing...")
    results = pool.starmap(test_compression, ratios)
    for i in sorted(results):
        if i[1] > 0.8:
            ratio = i[0]
            break

    final_image = image.resize((int(image.size[0]*ratio), int(image.size[1]*ratio)), PIL.Image.LANCZOS)
    final_image = final_image.resize((image.size[0], image.size[1]), PIL.Image.LANCZOS)
   
    return ratio, final_image

def CNN_compression(image):
    """
    A CNN approach to test the compression ratio of an image.
    Returns the ratio and the compressed image.
    Arguments:
        img: PIL.Image
        ratio: float
    Returns:
        ratio: float
        image: PIL.Image
    """
    model = model.CompressNet()
    model.load_state_dict(torch.load('./saved_models/model.pth'))
    model.eval()
    ratio = model.forward(image)
    final_image = image.resize((int(image.size[0]*ratio), int(image.size[1]*ratio)), PIL.Image.LANCZOS)
    final_image = final_image.resize((image.size[0], image.size[1]), PIL.Image.LANCZOS)
    return ratio, final_image

