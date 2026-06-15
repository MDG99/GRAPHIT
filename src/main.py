###

# Authors: 
    # - Ignacio Emmanuel Isaac Medina.
    # - Helbert Daniel Canché Sandoval.
    # - Francis Avilés Cetina.
    # - Alejandro Castillo Atoche.

# Date: Jun 2026.

###
import os
from graph import Graph
from writer import Writer
from reader import Reader
from skeleton import Skeleton
from morphology import Morphology


def main() -> None:
    """
        This function executes the main loop of the program.
    """
    # Read the images from a folder.
    folder_name = '../data'

    files = os.listdir(folder_name)
    
    for f in files:
        image_name = f[:-4]

        # 1. Initialize the writer object.
        writer = Writer(root='../results/', image_name=image_name)

        # 2. Read the input image and apply the grayscale conversion.
        reader = Reader(path='../data/', image_name=image_name + '.TIF')
        image = reader.image
        writer.save_image(image=image, image_name=image_name, suffix='Original')
        
        # 3. Apply the binarization (Otsu's algorithm)
        reader.process()
        image = reader.image
        writer.save_image(image=image, image_name=image_name, suffix='Binary')
        
        # 4. Apply morphological operations (Close)
        image = Morphology.close(image=image, kernel=3)
        writer.save_image(image=image, image_name=image_name, suffix='Close')

        # 5. Get the skeleton representation 
        image = Skeleton.choi_lam_siu(image=image, epsilon=20)
        writer.save_image(image=image, image_name=image_name, suffix='Skeleton')

        # 6. Graph
        graph = Graph(image=image, threshold_distance=5, digits=5)

        # 7. Parameters
        params = graph.get_parameters()
        writer.save_csv(filename='results.csv', params=params)

if __name__ == '__main__':
    main()