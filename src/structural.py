import cv2
import numpy as np
from scipy import ndimage

def draw_circles(image:np.ndarray, mask:np.ndarray, size:int=5) -> np.ndarray:
    rows, cols = np.shape(image)

    for row in range(rows):
        for col in range(cols):
            if mask[row, col] >= 1:
                cv2.circle(image, (col, row), size, (255, 255, 255), -1)
    
    return image

def apply_hit_or_miss(image:np.ndarray, structures:list) -> np.ndarray:
    result = np.zeros_like(image)
    
    for structure in structures:
        result = result + ndimage.binary_hit_or_miss(image, structure)

    return result

def get_endpoints(image:np.ndarray, circle_size:int=5) -> np.ndarray:

    endpoint_structures = [
        np.array([  [0, 0, 0],
                    [0, 1, 0],
                    [0, 1, 0]]),
        np.array([  [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 0, 0],
                    [0, 1, 1],
                    [0, 0, 0]]),
        np.array([  [0, 0, 1],
                    [0, 1, 0],
                    [0, 0, 0]]),
        np.array([  [0, 1, 0],
                    [0, 1, 0],
                    [0, 0, 0]]),
        np.array([  [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]]),
        np.array([  [0, 0, 0],
                    [1, 1, 0],
                    [0, 0, 0]]),
        np.array([  [0, 0, 0],
                    [0, 1, 0],
                    [1, 0, 0]]),
        np.array([  [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]]),
    ]

    mask = apply_hit_or_miss(image=image, structures=endpoint_structures)
    image = draw_circles(image=image, mask=mask, size=circle_size)

    return image

def get_intersections(image:np.ndarray, circle_size:int=5) -> np.ndarray:

    intersection_structures = [
        # Peaks
        np.array([  [1, 0, 0],
                    [0, 1, 0],
                    [1, 0, 0]]),
        np.array([  [1, 0, 1],
                    [0, 1, 0],
                    [0, 0, 0]]),
        np.array([  [0, 0, 1],
                    [0, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 0, 0],
                    [0, 1, 0],
                    [1, 0, 1]]),
        # Cross shapes
        np.array([  [1, 0, 1],
                    [0, 1, 0],
                    [1, 0, 1]]),
        np.array([  [0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]]),
        # Y-Shape
        np.array([  [1, 0, 0],
                    [0, 1, 1],
                    [1, 0, 0]]),
        np.array([  [1, 0, 1],
                    [0, 1, 0],
                    [0, 1, 0]]),
        np.array([  [0, 0, 1],
                    [1, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 1, 0],
                    [0, 1, 0],
                    [1, 0, 1]]),
        # T-Shape
        np.array([  [0, 1, 0],
                    [1, 1, 0],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]]),
        np.array([  [0, 1, 0],
                    [0, 1, 1],
                    [0, 1, 0]]),
        np.array([  [0, 0, 0],
                    [1, 1, 1],
                    [0, 1, 0]]),
        np.array([  [1, 0, 1],
                    [0, 1, 0],
                    [1, 0, 0]]),
        np.array([  [1, 0, 1],
                    [0, 1, 0],
                    [0, 0, 1]]),
        np.array([  [1, 0, 0],
                    [0, 1, 0],
                    [1, 0, 1]]),
        np.array([  [0, 0, 1],
                    [0, 1, 0],
                    [1, 0, 1]]),
        # Other variant 2
        np.array([  [0, 1, 0],
                    [1, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 1, 0],
                    [0, 1, 1],
                    [1, 0, 0]]),
        np.array([  [0, 0, 1],
                    [1, 1, 0],
                    [0, 1, 0]]),
        np.array([  [1, 0, 0],
                    [0, 1, 1],
                    [0, 1, 0]]),
        # Other variant 3
        np.array([  [0, 1, 0],
                    [1, 1, 0],
                    [1, 0, 1]]),
        np.array([  [1, 0, 1],
                    [1, 1, 0],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [0, 1, 1],
                    [1, 0, 1]]),
        np.array([  [1, 0, 1],
                    [0, 1, 1],
                    [0, 1, 0]]),
        np.array([  [0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 0, 1],
                    [1, 1, 0],
                    [0, 1, 1]]),
        np.array([  [1, 1, 0],
                    [0, 1, 1],
                    [1, 0, 0]]),
        np.array([  [1, 0, 0],
                    [0, 1, 1],
                    [1, 1, 0]]),
        # Cluster variants 1
        np.array([  [0, 1, 1],
                    [0, 1, 1],
                    [1, 0, 0]]),
        np.array([  [1, 0, 0],
                    [0, 1, 1],
                    [0, 1, 1]]),
        np.array([  [1, 1, 0],
                    [1, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 0, 1],
                    [1, 1, 0],
                    [1, 1, 0]]),
        # Cluster variants 2
        np.array([  [1, 1, 1],
                    [0, 1, 1],
                    [1, 0, 0]]),
        np.array([  [1, 0, 0],
                    [0, 1, 1],
                    [1, 1, 1]]),
        np.array([  [1, 1, 1],
                    [1, 1, 0],
                    [0, 0, 1]]),
        np.array([  [0, 0, 1],
                    [1, 1, 0],
                    [1, 1, 1]]),
        # Cluster variants 3
        np.array([  [1, 1, 1],
                    [0, 1, 1],
                    [1, 0, 1]]),
        np.array([  [1, 0, 1],
                    [0, 1, 1],
                    [1, 1, 1]]),
        np.array([  [1, 1, 1],
                    [1, 1, 0],
                    [1, 0, 1]]),
        np.array([  [1, 0, 1],
                    [1, 1, 0],
                    [1, 1, 1]]),
        # Composed cross variant 1
        np.array([  [1, 0, 0],
                    [1, 1, 1],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [1, 1, 1],
                    [1, 0, 0]]),
        np.array([  [0, 0, 1],
                    [1, 1, 1],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 1]]),
        # Composed cross variant 2
        np.array([  [1, 1, 0],
                    [0, 1, 1],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [0, 1, 1],
                    [1, 1, 0]]),
        np.array([  [0, 1, 1],
                    [1, 1, 0],
                    [0, 1, 0]]),
        np.array([  [0, 1, 0],
                    [1, 1, 0],
                    [0, 1, 1]]),
        # Special variants (4-lenght)
        np.array([  [1,0,0,1],
                    [0,1,1,0],
                    [0,0,0,0],
                    [0,0,0,0]]),
        np.array([  [0,0,0,1],
                    [0,0,1,0],
                    [0,0,1,0],
                    [0,0,0,1]]),
        np.array([  [0,0,0,0],
                    [0,0,0,0],
                    [0,1,1,0],
                    [1,0,0,1]]),
        np.array([  [1,0,0,0],
                    [0,1,0,0],
                    [0,1,0,0],
                    [1,0,0,0]]),
        # Special variants (4-lenght) #TODO: Check this variant
        np.array([  [0,1,0,0,0],
                    [0,1,0,0,0],
                    [0,0,1,1,0],
                    [0,0,0,0,1],
                    [0,0,0,0,0]]),
        # Special variants (5-lenght)
        np.array([  [1,0,0,0,0],
                    [0,1,0,0,0],
                    [0,1,0,0,0],
                    [0,1,0,0,0],
                    [1,0,0,0,0]]),
        np.array([  [1,0,0,0,1],
                    [0,1,1,1,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]),
        np.array([  [0,0,0,0,1],
                    [0,0,0,1,0],
                    [0,0,0,1,0],
                    [0,0,0,1,0],
                    [0,0,0,0,1]]),
        np.array([  [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,1,1,1,0],
                    [1,0,0,0,1]]),
        # special variantes (9-lenght)
        np.array([  [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [1,1,1,1,1,0,0,0,0],
                    [0,0,0,0,0,1,1,0,0],
                    [0,0,0,0,0,0,0,1,1],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0]]),
        # special variantes (9-lenght)
        np.array([  [1,0,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0]])
    ]

    mask = apply_hit_or_miss(image=image, structures=intersection_structures)
    image = draw_circles(image=image, mask=mask, size=circle_size)

    return image