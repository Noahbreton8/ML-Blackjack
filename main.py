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
WIDTH, HEIGHT = 1280, 1024
capture.set(3,  WIDTH)
capture.set(4, HEIGHT)

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

if not os.path.exists('images'):
    os.makedirs('images')

while (True):
    _, frame = capture.read()

    cv.line(frame, (0, int(HEIGHT/3)), (WIDTH, int(HEIGHT/3)), (0, 255, 0), 2)
    for i in range(1, 4):
        cv.line(frame, (int(WIDTH*i/4), 0), (int(WIDTH*i/4), HEIGHT), (0, 255, 0), 2)

    cv.imshow('stream', frame)

    fgMask = backSub.apply(frame, learningRate=0)

    # cv.imshow('FG Mask', fgMask)

    if cv.waitKey(1) == ord('b'):
        cv.imwrite('images/bg.png', frame)
    if cv.waitKey(1) == ord('s'):
        cv.imwrite('images/cam.png', frame)
    if cv.waitKey(1) == ord('l'):
        partitions = []
        for i in range(3):
            for j in range(4):
                partitions.append(frame[int(HEIGHT/3)*i:int(HEIGHT/3)*(i+1), int(WIDTH/4)*j:int(WIDTH/4)*(j+1)])    

        for part in partitions:
            cv.imwrite(f'images/partition_{part}.png', part)
        print('Saved partitions')

    elif cv.waitKey(1) == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()