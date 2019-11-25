import cv2

def show_webcam(mirror=False):
    scale=50

    cam = cv2.VideoCapture(0)
    make_1080(cam)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)


        #get the webcam size
        height, width, channels = img.shape

        #prepare the crop
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)

        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY

        cropped = img[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height)) 

        #resized_cropped = rescale_frame(resized_cropped)
        cv2.imshow('my webcam', resized_cropped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # esc to quit

        #add + or - 5 % to zoom

        if cv2.waitKey(1) & 0xFF == ord('a'):
            scale -= 10  # +5

        if cv2.waitKey(1) & 0xFF == ord('b'):
            scale = 50  # +5

    cv2.destroyAllWindows()

def make_1080(cam):
    cam.set(3, 1920)
    cam.set(4, 1080)

def make_480(cam):
    cam.set(3, 640)
    cam.set(4, 480)

def rescale_frame(frame, percent=200):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()