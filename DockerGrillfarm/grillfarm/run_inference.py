import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
from detectron2.data import MetadataCatalog

from detectron2.utils.logger import setup_logger
setup_logger() # this logs Detectron2 information such as what the model is doing when it's training

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor # a default predictor class to make predictions on an image using a trained model
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode# a class to help visualize Detectron2 predictions on an image
 # stores information about the model such as what the training/test data is, what the class names are
import numpy as np
import configure_model

#get all data in textform
from detectron2.utils.visualizer import _create_text_labels
cfg = configure_model.configure_model()
predictor = DefaultPredictor(cfg)
def textinference(target_classes, image):
    v = Visualizer(image[:, :, ::-1],
                   metadata=MetadataCatalog.get(cfg.DATASETS.TEST[0]).set(thing_classes=target_classes), \
                   scale=0.8, \
                   instance_mode=ColorMode.IMAGE_BW)
    outputs = predictor(image)
    predictions =outputs['instances'].to('cpu')
    boxes = predictions.pred_boxes if predictions.has("pred_boxes") else None
    scores = predictions.scores if predictions.has("scores") else None
    classes = predictions.pred_classes.tolist() if predictions.has("pred_classes") else None
    labels = _create_text_labels(classes, scores, v.metadata.get("thing_classes", None))

    if predictions.has("pred_masks"):
      masks = np.asarray(predictions.pred_masks)
    else:
      masks = None
    return boxes, scores, classes, labels, masks