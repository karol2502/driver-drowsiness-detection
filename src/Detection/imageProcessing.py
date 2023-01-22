import cv2
import os


class ImageProcessing:
    def __init__(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
            self.eye_cascade = cv2.CascadeClassifier(os.path.join(self.cv2_base_dir, 'data\\haarcascade_eye.xml'))
            self.face_cascade = cv2.CascadeClassifier(os.path.join(self.cv2_base_dir, 'data\\haarcascade_frontalface_default.xml'))
            self.font = cv2.FONT_HERSHEY_SIMPLEX
        except Exception as e:
            print(e)

    def is_camera_opened(self):
        return self.camera.isOpened()

    def get_image(self):
        ret, img = self.camera.read()
        return img

    def destroy(self):
        self.camera.release()
        cv2.destroyAllWindows()
