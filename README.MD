# GRAPHIT (GRAPH Interconnectivity Tool)

This repository contains the source code for GRAPHIT, a tool designed to quantify the interconnectivity of electrical networks. It serves as complementary data and software for the paper " Quantifying electrical network interconnectivity using graph theory” by H. Canché-Sandoval, I. Isaac-Medina, O. Solís-Canto, A. Castillo-Atoche, and F. Avilés.

## Repository Structure

The repository is organized as follows:

* `src/`: Contains the Python scripts required to perform each processing stage.

## Prerequisites

This software requires Python 3.11 or higher.

The required libraries are listed below and can be easily installed using the provided requirements.txt file:

* `networkx==3.6.1`
* `numpy==2.4.6`
* `opencv-python==4.13.0.92`
* `pandas==3.0.3`
* `scikit-image==0.26.0`
* `scipy==1.17.1`
* `skan==0.13.1`

## Getting Started

To start using the GRAPHIT software, follow these steps:

1.  **Set up your environment:** It is recommended to create and activate a new virtual environment:
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Prepare the data directory:** Create a directory named `data/` in the root of this project (if it does not already exist).
4.  **Upload images:** Place the images you wish to analyze inside the `data/` folder.
5.  **Navigate to the source directory:**
    ```bash
        cd src
    ```
6.  **Execute the software:** Run the main script from your terminal:
    ```bash
    python main.py
    ```
7.  **Monitor the console:** In the terminal, you will see a message indicating the specific folder created for each processed image. The naming convention for these output folders is: 
    `YYYYMMDDHHmmsss_ImageName`
8.  **Review the output:** Navigate to the `results/` directory. Inside, you will find subdirectories for each image containing the following files:
    * `ImageName_1_Original.jpg`: A copy of the source image under analysis.
    * `ImageName_2_Binary.jpg`: The result after applying the binary operation.
    * `ImageName_3_Close.jpg`: The image obtained after applying the closing morphological operation.
    * `ImageName_4_Skeleton.jpg`: The resulting skeletonized network.
    * `results.csv`: Contains the calculated interconnectivity parameters for the image.

## Example

The following sequence demonstrates the standard image processing pipeline performed by the software. For a given input, GRAPHIT generates four distinct images representing each stage of the analysis:

<div align="center">
  <img src="doc/results_example.png"/>
</div>
<div align="center">
  <em> Expected results: a) Original, b) Binary, c) Morphological Close, and d) Skeletonized network.</em>
</div>

## Notes

The final interconnectivity results may depend on the specific parameters used during the skeletonization and morphological operations. These parameters can be manually adjusted within the `src/` scripts to fit different image types or polymer network densities.

## License

This software and associated code are distributed under the **MIT License**. Please refer to the `LICENSE` file for full details.

## Authorship

* **Contributors:**
    * Helbert D. Canché-Sandoval (Centro de Investigación Científica de Yucatán A.C.)
    * Ignacio E. Isaac Medina (Centro de Investigación Científica de Yucatán A.C.)
    * Alejandro Castillo Atoche (Universidad Autónoma de Yucatán)
    * Francis Avilés Cetina (Centro de Investigación Científica de Yucatán A.C.)
* **Contact:** faviles@cicy.mx
* **Publishing date:** July 2026
* **Acknowledgements:** Work supported by SECIHTI (Mexico) under grant number CF-2023-I-926.

## Citation

If you use this code or methodology for your research, please cite it using the format provided in the `CITATION.bib` file.
