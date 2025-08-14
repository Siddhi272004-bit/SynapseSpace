import cv2 as cv
import numpy as np

# Initialize color components
r, g, b = 0, 0, 0

# Mouse drawing variables
drawing = False
mode = True  # True: Rectangle, False: Circle/Freehand
ix, iy = -1, -1

# Mouse callback function
def draw(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, r, g, b

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                temp_img = img.copy()
                cv.rectangle(temp_img, (ix, iy), (x, y), (b, g, r), -1)
                cv.imshow('Canvas', temp_img)
            else:
                cv.circle(img, (x, y), 3, (b, g, r), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv.rectangle(img, (ix, iy), (x, y), (b, g, r), -1)
        else:
            cv.circle(img, (x, y), 3, (b, g, r), -1)

# Trackbar callback
def nothing(x):
    pass

# Create a white canvas
img = np.ones((512, 512, 3), np.uint8) * 255
cv.namedWindow('Canvas')
cv.setMouseCallback('Canvas', draw)

# Create trackbars for R, G, B
cv.createTrackbar('R', 'Canvas', 0, 255, nothing)
cv.createTrackbar('G', 'Canvas', 0, 255, nothing)
cv.createTrackbar('B', 'Canvas', 0, 255, nothing)

while True:
    # Update current RGB values from trackbars
    r = cv.getTrackbarPos('R', 'Canvas')
    g = cv.getTrackbarPos('G', 'Canvas')
    b = cv.getTrackbarPos('B', 'Canvas')

    cv.imshow('Canvas', img)
    key = cv.waitKey(1) & 0xFF

    if key == ord('m'):
        mode = not mode  # toggle mode
    elif key == ord('s'):
        cv.imwrite('drawing.png', img)
        print("✅ Drawing saved as drawing.png")
    elif key == 27:  # ESC
        break

cv.destroyAllWindows()
