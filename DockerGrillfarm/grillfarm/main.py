import run_on_video
import run_inference
import cv2
import os
import sys, getopt
import json


def main(argv):
    idir = ''
    odir = ''
    mode = ''
    frames = ''
    try:
        opts, args = getopt.getopt(argv,'hv:m:i:o:f:')
    except getopt.GetoptError:
        print ('main.py -v <inputdirvid> -m <data/check> -o <outputdir> -f <percentage of input_frames> -i <textinference on image>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -v <inputdirvid> -m <data/check> -o <outputdir> -f <percentage of input_frames> -i <textinference on image>')
            sys.exit()
        if opt in ('-v'):
            idir = arg, 'video'
        elif opt in ('-m'):
            mode = arg
        elif opt in ('-i'):
            idir = arg, 'image'
        elif opt in ('-o'):
            odir = arg
        elif opt in ('-f'):
            frames = arg
    return idir, odir, mode, frames

inputinf, outputdir, vidmode, frames = main(sys.argv[1:])
print('inputinf: ' + str(inputinf) + 'outputdir: ' + str(outputdir) + 'vidmode: ' + vidmode + 'frames: ' + frames)
try:
    os.mkdir(outputdir)
except OSError:
    print ('Creation of the directory %s failed' % outputdir)
else:
    print ('Successfully created the directory %s ' % outputdir)
inputdir, mode = inputinf
target_classes = ['moving', 'juvenile', 'damaged_adult_male', 'damaged_adult_female', 'adult_female', 'cannibalism', 'egg_laying_female', 'adult_male']
if mode == 'video':
    run_on_video.RunOnVideo.initialize_run(target_classes, vidmode, inputdir, frames, outputdir )
elif mode == 'image':
    dictionary = {}
    x=1
    for item in os.listdir(inputdir):
        im = cv2.imread(inputdir + '/' + item)
        boxes, scores, classes, labels, masks = run_inference.textinference(target_classes, im)
        print('!Boxes: ' + str(boxes) +  '\n!Scores: ' + str(scores) + '\n!Classes: ' + str(classes) +  '\n!Labels: ' + str(labels) + '\n!Maks: ' + str(masks))
        break
        dictionary['boxes'].append(boxes)
        dictionary['scores'].append(scores)
        dictionary['classes'].append(classes)
        dictionary['labels'].append(labels)
        dictionary['masks'].append(masks)
    
        iter = x + '.json'
        
        with open(outputdir/iter, 'w') as json_file:
            json.dump(dictionary, json_file)
        x+=1



