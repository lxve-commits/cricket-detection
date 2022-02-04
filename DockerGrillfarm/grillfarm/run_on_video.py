# import some common libraries
import numpy as np
import tqdm
import cv2
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.data import MetadataCatalog
import time
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import configure_model
import run_inference
import json

class RunOnVideo:
    def run_on_video(self, video, maxFrames, predictor):
        ''' Runs the predictor on every frame in the video (unless maxFrames is given),
        and returns the frame with the predictions drawn.
        '''

        readFrames = 0
        while True:
            has_frame, frame = video.read()
            if not has_frame:
                break

            # Get prediction results for this frame
            outputs = predictor(frame)

            # Make sure the frame is colored
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Draw a visualization of the predictions using the video visualizer
            visualization = self.draw_instance_predictions(frame, outputs['instances'].to('cpu'))

            # Convert Matplotlib RGB format to OpenCV BGR format
            visualization = cv2.cvtColor(visualization.get_image(), cv2.COLOR_RGB2BGR)

            yield visualization

            readFrames += 1
            if readFrames > maxFrames:
                break
    def initialize_run (self, mode, path, max_frames, outputdir):
        target_classes = self
        cfg = configure_model.configure_model()
        predictor = DefaultPredictor(cfg)
        # Extract video properties
        video = cv2.VideoCapture(path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if mode == 'data':
            dictionary = {}
            x=0
            while True:
                print(str(x) + '>' + str(float(max_frames)*float(num_frames)))
                has_frame, frame = video.read()
                if not has_frame:
                    break
                boxes, scores, classes, labels, masks = run_inference.textinference(target_classes, frame)
                if 'frameNumber' in dictionary:
                    dictionary['frameNumber'].append(x)
                else:
                    dictionary['frameNumber'] = [x]
                if 'boxes' in dictionary:
                    dictionary['boxes'].append(str(boxes))
                else:
                    dictionary['boxes'] = [str(boxes)]
                if 'scores' in dictionary:
                    dictionary['scores'].append(str(scores))
                else:
                    dictionary['scores'] = [str(scores)]
                if 'classes' in dictionary:
                    dictionary['classes'].append(str(classes))
                else:
                    dictionary['classes'] = [str(classes)]
                if 'labels' in dictionary:
                    dictionary['labels'].append(str(labels))
                else:
                    dictionary['labels'] = [str(labels)]
                if 'masks' in dictionary:
                    dictionary['masks'].append(str(masks))
                else:
                    dictionary['masks'] = [str(masks)]
            
                iter = str(x) + '.json'
                if float(x) > float(max_frames)*float(num_frames):
                    break
                x+=1
            with open(outputdir + '/' + iter, 'w') as json_file:
                json.dump(dictionary, json_file)
            
            # Release resources
            video.release()
            cv2.destroyAllWindows()
        
        # Initialize video writer
        elif mode == 'check':
            video_writer = cv2.VideoWriter(outputdir + '_inference.mp4', fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=float(frames_per_second), frameSize=(width, height), isColor=True)
            # Initialize visualizer
            # v = VideoVisualizer(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), ColorMode.IMAGE)
                    
            v = VideoVisualizer(metadata=MetadataCatalog.get(cfg.DATASETS.TEST[0]).set(thing_classes=target_classes),
                                instance_mode=ColorMode.IMAGE_BW)

            # Create a cut-off for debugging

            # Enumerate the frames of the video
            for visualization in tqdm.tqdm(RunOnVideo.run_on_video(v, video, float(max_frames)*float(num_frames), predictor), total=num_frames):
                # Write test image

                # Write to video file
                video_writer.write(visualization)

            # Release resources
            video.release()
            video_writer.release()
            cv2.destroyAllWindows()
            return outputdir + '_inference.mp4'
