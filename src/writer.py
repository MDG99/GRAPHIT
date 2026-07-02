import os
import cv2
import numpy as np
import datetime as dt
import pandas as pd

class Writer:
    """
    A class for managing the writing operations.

    Attributes
    ----------
    path : str
        folder where the results will be stored.
    
    Methods
    -------
    save_image:
        Save a given imagen in the main results folder.
    save_csv:
        Save a dictionary with the calculated params into a CSV file.
    """

    def __init__(self, root:str='../results/', image_name:str='') -> None:
        """
        Constructs all the necessary attributes for reading and preprocessing the input image. It includes an exception if the file does not exist.

        Parameters
        ----------
            root : str ('results')
                root folder used to save the results.
            image_name : int ('')
                image name, without the extension.
        """   
        self.id = 1
        self.root = root
        self.path = root + dt.datetime.now().strftime("%Y%m%d%H%M%S") + '_' +image_name
        os.makedirs(self.path)

        print(f"Results folder {self.path} created.")
    
    def save_image(self, image_name:str='', suffix:str='', image:np.array=None):
        """
        Save an image using the following name convention: image_name + step + suffix.

        Parameters
        ----------
            image_name : str ('')
                image name.
            suffix : str ('results')
                brief description of the current step.
            image : np.array | None (None)
                image to be saved.

        Returns
        -------
            None.
        """

        if image_name != '' and image_name != None:
            cv2.imwrite(self.path + '/' + image_name + f'_{self.id}_' + suffix + '.jpg', image)
            self.id += 1

    def save_csv(self, filename:str='results.csv', params:dict={}):
        """
        Save the calculated params into a csv file.

        Parameters
        ----------
            filename : str ('results.csv')
                file name of the csv file (including the extension).
            params : dict ({})
                dictionary with the calculated graph params.

        Returns
        -------
            None.
        """

        if len(params) > 0 :
            pd.DataFrame(params).to_csv(self.path + '/' + filename, index=False)