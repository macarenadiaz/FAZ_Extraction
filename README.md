# Automatic FAZ Extraction
This code contains a method to extract the Foveal Avascular Zone (FAZ) in OCT-A images using morphological operators, edge detectors and regiong growing. 
For more information about the dataset features, see www.varpa.org/research/ophtalmology.html. Also, you can request the OCTAGON dataset by mail (macarena.diaz1@udc.es). Please, if you use this code or the OCTAGON dataset, cite our papers as follows:
- M. Díaz, J. Novo, P. Cutrín, F. Gómez-Ulla, M. G. Penedo, M. Ortega, "Automatic segmentation of the Foveal Avascular Zone in ophtalmological OCT-A images", PLoS One, 14(2), e0212364, 2019. You can read this paper to understand the steps of this code or to compare wit your results (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0212364).
- M. Díaz, J. Novo, M. G. Penedo, M. Ortega, "Automatic extraction of vascularity measurements using OCT-A images", Knowledge-Based and Intelligent Information & Engineering Systems: Proceedings of the 22st International Conference, KES-2018, 126, 273-281, Belgrado, Serbia, September	2018. (https://www.sciencedirect.com/science/article/pii/S1877050918312377)

## Requirements

### Python
We use python 2.7 in this version but we are working to update the implementation to provide the implementation in the last version (python 3.6).

- [numpy](https://docs.scipy.org/doc/numpy-1.13.0/user/install.html)
- [opencv](https://opencv.org/)
- [matplotlib](https://matplotlib.org/)
- [scikit-image](https://scikit-image.org/)
