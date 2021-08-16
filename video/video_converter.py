import cv2
import os

if __name__ == "__main__":

    video = cv2.VideoCapture(r'/home/musashi/Documents/proyectos/python/assets/video_mujer_sin:cabeza.mp4')
    try:
        if not os.path.exists('bruja'):
            os.makedirs('bruja')
    except OSError:
        print('Error')
    currentframe = 0
    while True:
        ret, frame = video.read()

        if ret:
            name = './bruja/frame' + str(currentframe) + '.jpg'
            print('Captured...' + name)
            cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break
    video.release()
    cv2.destroyAllWindows()
