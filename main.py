import cv2 as cv
from cv2.typing import MatLike
import os
from gameStrategy import tts

#tts
tts = tts.TTS()

# set up video capture
capture = cv.VideoCapture(0) #Might need to change to 1
WIDTH, HEIGHT = 1280, 1024
capture.set(3,  WIDTH)
capture.set(4, HEIGHT)

if not os.path.exists('images'):
    os.makedirs('images')


def contains_card(frame: MatLike) -> bool:
    WHITE_BOUND = 120
    width = frame.shape[1] #320
    height = frame.shape[0] #341
    matchesRequired = 25000 #max pixel count is around 109,000
    pixelMatches = 0

    for y in range(0, width):
        for x in range(0, height):
            (blue, green, red) = frame[x, y]
            # print(f"RGB: {red}, {green}, {blue}")

            if blue >= WHITE_BOUND and green >= WHITE_BOUND and red >= WHITE_BOUND:
                pixelMatches += 1
            # works = True
            # for k in color:
            #     if not (whiteRange[0] > k and k < whiteRange[1]):
            #         works = False
            # if works:
            #     #print("pixel matches ", pixelMatches)
            #     pixelMatches += 1
            if pixelMatches >= matchesRequired:
                return True
    return False



while (True):
    _, frame = capture.read()

    if cv.waitKey(5) == ord('b'):
        cv.imwrite('./images/bg.png', frame)
    if cv.waitKey(5) == ord('s'):
        cv.imwrite('./images/cam.png', frame)
    if cv.waitKey(5) == ord('l'):
        partitions = []
        for i in range(3):
            for j in range(4):
                partitions.append(frame[int(HEIGHT/3)*i:int(HEIGHT/3)*(i+1), int(WIDTH/4)*j:int(WIDTH/4)*(j+1)])    

        for i in range(0, 8):
            if contains_card(partitions[i]):
                yes_str = f"{i}: CONTAINS A CARD!"
                print(yes_str)
                tts.speak(yes_str)
            else:
                no_str = f"{i}: FUCKING DOESNT"
                print(no_str)
                tts.speak(no_str)
            cv.imwrite(f'./images/partition_{i}.png', partitions[i])
        print()

    # alignment guides
    cv.line(frame, (0, int(HEIGHT/3)), (WIDTH, int(HEIGHT/3)), (0, 255, 0), 2)
    for i in range(1, 4):
        cv.line(frame, (int(WIDTH*i/4), 0), (int(WIDTH*i/4), HEIGHT), (0, 255, 0), 2)

    cv.imshow('stream', frame)

    if cv.waitKey(5) == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()

# def test_2():
#     # read the input image
#     image = cv.imread('./images/partition_1.png')

#     # define the alpha and beta
#     alpha = 0.5 # Contrast control
#     beta = -70 # Brightness control

#     # call convertScaleAbs function
#     adjusted = cv.convertScaleAbs(image, alpha=alpha, beta=beta)

#     # display the output image
#     cv.imwrite('adjusted_2_9.png', adjusted)

# test_2()