

class ModelOutput():
    """Output for a single study.
    Args:
        image (str): A path to dicom images.
        class_probabilities (dict): Dictionary of key value pairs of diagnoses and probability that this diagnosis matches the image.
        mask (str): A path to a numpy mask.
        display (str): A summary of the outpuer

    Attributes:
        image (str): A path to dicom images.
        class_probabilities (dict): Dictionary of key value pairs of diagnoses and probability that this diagnosis matches the image.
        mask (str): A path to a numpy mask.
        display (str): A summary of the outpuer
    """ 



    
    def __init__(self, image=None, class_probabilities=None, mask=None, display=''):
        self.image = image
        self.class_probabilities = class_probabilities
        self.mask = mask
        self.display = display


    def __repr__(self):
        """Repr
        print function will return display attributes
        """

        return self.display