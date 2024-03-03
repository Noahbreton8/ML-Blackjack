import cv2 as cv
import argparse
import os

#MOG subtraction stuff
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

# set up video capture
capture = cv.VideoCapture(0)
length, width = 1280, 1024
capture.set(3,  length)
capture.set(4, width)

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

if not os.path.exists('images'):
    os.makedirs('images')





while (True):
    _, frame = capture.read()

    cv.line(frame, (int(length/2), 0), (int(length/2), width), (0, 255, 0), 2)
    # for i in range(1, 5):
        # cv.line(frame, (int(length/i), 0), (int(length/i), width), (0, 255, 0), 2)

    cv.imshow('stream', frame)

    fgMask = backSub.apply(frame, learningRate=0)

    cv.imshow('FG Mask', fgMask)

    if cv.waitKey(1) == ord('b'):
        cv.imwrite('images/bg.png', frame)
    elif cv.waitKey(1) == ord('s'):
        cv.imwrite('images/cam.png', frame)
    elif cv.waitKey(1) == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()