import cv2
import numpy as np


class Morphology:
    """
    Static class with a list of morphological operations.

    Methods
    -------
    dilate:
        performs the dilatation operation.
    erode:
        performs the erosion operation.
    open_:
        performs the closing operation (erosion + dilatation).
    close:
        performs the opening operation (dilatation + erosion).
    """
    
    @staticmethod
    def dilate(image:np.ndarray, kernel:int=3) -> np.ndarray:
        """
        Performs the dilatation operation in a given image.

        Parameters
        ----------
            image : np.ndarray.
                image to apply the morphological operation.
            kernel : int (3)
                window size.

        Returns
        -------
            np.ndarray : image after performing the dilatation.
        """
        return cv2.dilate(image, kernel=np.ones((kernel,kernel),np.uint8))
    
    @staticmethod
    def erode(image:np.ndarray, kernel:int=3) -> np.ndarray:
        """
        Performs the erosion operation in a given image.

        Parameters
        ----------
            image : np.ndarray.
                image to apply the morphological operation.
            kernel : int (3)
                window size.

        Returns
        -------
            np.ndarray : image after performing the erosion.
        """
        return cv2.erode(image, kernel=np.ones((kernel,kernel),np.uint8))
    
    @staticmethod
    def open_(image:np.ndarray, kernel:int=3) -> np.ndarray:
        """
        Performs the opening operation in a given image.

        Parameters
        ----------
            image : np.ndarray.
                image to apply the morphological operation.
            kernel : int (3)
                window size.

        Returns
        -------
            np.ndarray : image after performing the opening.
        """
        image_inter =  cv2.erode(image, kernel=np.ones((kernel,kernel),np.uint8))
        return cv2.dilate(image_inter, kernel=np.ones((kernel,kernel),np.uint8))
    
    @staticmethod
    def close(image:np.ndarray, kernel:int=3) -> np.ndarray:
        """
        Performs the closing operation in a given image.

        Parameters
        ----------
            image : np.ndarray.
                image to apply the morphological operation.
            kernel : int (3)
                window size.

        Returns
        -------
            np.ndarray : image after performing the closing.
        """
        image_inter =  cv2.dilate(image, kernel=np.ones((kernel,kernel),np.uint8))
        return cv2.erode(image_inter, kernel=np.ones((kernel,kernel),np.uint8))