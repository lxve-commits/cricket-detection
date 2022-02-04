import detectron2
from detectron2 import config
from detectron2.config import get_cfg

from detectron2.utils.logger import setup_logger
setup_logger() # this logs Detectron2 information such as what the model is doing when it's training

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor # a default predictor class to make predictions on an image using a trained model
def configure_model():
    cfg = get_cfg()
    cfg.merge_from_file("/trained_model/config.yml",
                    False)  # merge the config YAML file (a set of instructions on how to build a model)
    cfg.MODEL.WEIGHTS = "/trained_model/trained_model.pth"  # setup the model weights from the fully trained model
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.DEVICE = "cpu"
    return cfg
