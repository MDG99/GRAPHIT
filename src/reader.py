import os
import cv2


class Reader:
    """
    A class for managing reading operations and preprocess the image.

    ...

    Attributes
    ----------
    path : str
        folder where is stored the input data.
    is_inverse : bool
        flag used to perform the binarization using the inverse operation.
    image_name : str
        image name, including the extension.
    full_path : str
        concatenation of the input data and image name.
    image : array
        image read.

    Methods
    -------
    process:
        perfomrs the preprocessing operations: read, grayscale and binarization (Otsu's algorithm).
    """


    def __init__(self, path:str='./data/', image_name:str='', is_inverse:bool=False) -> None:
        """
        Constructs all the necessary attributes for reading and preprocessing the input image. It includes an exception if the file does not exist.

        Parameters
        ----------
            path : str ('..\data')
                folder where is stored the input data.
            results_path : str ('results')
                root folder used to save the results.
            image_name : int ('')
                image name, including the extension.
            is_inverse : bool (False)
                flag used to perform the binarization using the inverse operation.
        """   

        self.path = path
        self.is_inverse = is_inverse
        self.image_name = image_name
        
        self.full_path = self.path + self.image_name

        if not os.path.isfile(self.full_path):
            raise FileNotFoundError(f'ERROR: The input image "{self.full_path}" does not exist.')
        
        self.image = cv2.imread(self.full_path, cv2.IMREAD_COLOR)
    
    def process(self) -> None:
        """
        Perform the image preprocessing stage: grayscale conversion, and binarization using Otsu's algoritm.

        If the is_inverse bool is True, the binarization is performed in invers mode (black pixels are ground truth).

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        th_type = cv2.THRESH_BINARY_INV if self.is_inverse else cv2.THRESH_BINARY
        th_type += cv2.THRESH_OTSU
        
        self.image = cv2.threshold(self.image, 0, 255, th_type)[1]