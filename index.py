import cv2
import os
import sys

video = cv2.VideoCapture("video.mp4")

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

asciiValues = "$@B%8&WM#oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`\'. "

def grayscaleValueToAscii(value):
    value = 255 - value
    index = int((value/255)*len(asciiValues)) - 1
    return asciiValues[index]

def pixelFrameToAscii(frame):
    newFrame=[]
    for y in range(0, height-1, 3):
        row = []
        for x in range(0, width-1, 3):
            cumulativeValue = 0
            cumulativeValue += (frame[y][x] + frame[y][x + 1] + frame[y][x + 2])
            cumulativeValue += (frame[y + 1][x] + frame[y + 1][x + 1] + frame[y + 1][x + 2])
            cumulativeValue += (frame[y + 2][x] + frame[y + 2][x + 1] + frame[y + 2][x + 2])
            row.append(grayscaleValueToAscii(cumulativeValue/9))
        newFrame.append(row)
    return newFrame

def writeFrame(frame):
    sys.stdout.write("\033[H")  # Move cursor to top-left (better than clearing screen)
    for row in frame:
        for val in row:
            sys.stdout.write(val + " ")
        sys.stdout.write("\n")


while True:
    successfulFrameRead, frame = video.read()
    if not successfulFrameRead:
        break  # Exit if video ends
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    asciiFrame = pixelFrameToAscii(frame)
    writeFrame(asciiFrame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    #os.system("cls")

video.release()
cv2.destroyAllWindows()