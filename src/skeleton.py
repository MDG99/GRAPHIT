import numpy as np

from scipy import ndimage
from skimage.morphology import skeletonize


class Skeleton:
    """
    Static class with a list of skeletonization algorithms availables.

    Methods
    -------
    zhang_suen:
        performs the Zhang and suen algorithm.
    choi_lam_siu:
        performs the Choi, Lam and Siu algorithm.
    """

    @staticmethod
    def zhang_suen(image:np.ndarray) -> np.ndarray:
        """
        Performs the Zhang and Suen thinning algorithm to get the representative skeleton.

        Reference: https://doi.org/10.1145/357994.358023
        
        Parameters
        ----------
            image : np.ndarray.
                binary input image.

        Returns
        -------
            np.ndarray : representative skeleton.
        """
        return skeletonize(~image).astype(np.uint8)*255
    
    @staticmethod
    def choi_lam_siu(image:np.ndarray, epsilon:float=20.0) -> np.ndarray:
        """
        Performs the Choi, Lam and Siu skeleton algorithm to get the representative skeleton.

        Reference: https://doi.org/10.1016/S0031-3203(02)00098-5
        
        Parameters
        ----------
            image : np.ndarray.
                binary input image.
            epsilon : float (20.0)
                control parameter.

        Returns
        -------
            np.ndarray : representative skeleton.
        """
        
        # Map of distances and cotourn points.
        image = ~image  
        image = image*255

        _, (yi, xi) = ndimage.distance_transform_edt(image, return_indices=True)

        # Initial calculation of pixel indexes.
        obj_pixels = np.argwhere(image == 1)

        # Offsets for 8 neighbors.
        offsets = [ (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        # Skeleton initialization.
        skeleton = np.zeros_like(image, dtype=np.uint8)

        # Processing object pixels.
        for i, j in obj_pixels:
            if i == 0 or i == image.shape[0]-1 or j == 0 or j == image.shape[1]-1:
                continue  # skiping borders

            # Q value
            q_y, q_x = yi[i, j], xi[i, j]

            # Calculation of Qi for all neighbors
            neighbors = []
            for dx, dy in offsets:
                x, y = i + dx, j + dy
                if 0 <= x < image.shape[0] and 0 <= y < image.shape[1] and image[x, y] == 1:
                    qi_y, qi_x = yi[x, y], xi[x, y]
                    neighbors.append((qi_y, qi_x))

            # Applying the connectivity creteria
            if neighbors:
                qi = np.array(neighbors)
                Q = np.array([q_y, q_x])

                # Optimized calculations
                D2 = ((qi - Q)**2).sum(axis=1)
                diff_norm = (qi[:, 0]**2 + qi[:, 1]**2) - (Q[0]**2 + Q[1]**2)
                max_diff = np.maximum(np.abs(qi[:, 0] - Q[0]), np.abs(qi[:, 1] - Q[1]))

                if np.any((D2 > epsilon) & (diff_norm <= max_diff)):
                    skeleton[i, j] = 255
        
        return skeleton