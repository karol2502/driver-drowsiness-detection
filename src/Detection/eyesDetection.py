import cv2
from PIL import Image
import torch
from torchvision import transforms
from Detection.cnn2 import cnn2
from Detection.detectionModel import DetectionModel
from PySide6.QtCore import QObject
import time
import winsound

from Detection.imageProcessing import ImageProcessing

class DetectionState:
    Open = 0
    Closed = 1
    Undetected = 2


class EyesDetection(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.image_processing = ImageProcessing()
        self.device = 'cpu'

        self.cnn2 = cnn2()
        DetectionModel.load(self.cnn2)

        self.model = self.cnn2

        self.model.eval()
        self.model.to(self.device)

        self.score = 0.0
        self.detecting_state = False
        self.elapsed_time = 0.0
        self.detected_closed = False

    @classmethod
    def train_transforms(clc, frame):
        return transforms.Compose(
        [
            transforms.Resize(80),
            transforms.ToTensor()
        ])(frame)

    def detect(self):
        img = cv2.resize(self.image_processing.get_image(), (int(self.image_processing.camera.get(3) // 1.5), int(self.image_processing.camera.get(4) // 1.5)))
        # img = self.image_processing.get_image()

        preds = []
        eyes = self.image_processing.eye_cascade.detectMultiScale(img, 1.1, 9)

        for (ex,ey,ew,eh) in eyes:
            color = img[ey:ey+eh, ex:ex+ew]
            cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            frame = Image.fromarray(color)
            frame = self.train_transforms(frame)
            frame = frame.to(self.device)
            frame = frame.reshape(1,3,80,80)
            pred = self.model(frame)
            pred = torch.argmax(pred, dim=1)
            preds.append(pred.detach().cpu())

        if len(preds) == 0:
            detectionState = DetectionState.Undetected
        else:
            if 1 in preds:
                detectionState = DetectionState.Open
                if self.score > 0:
                    self.score -= 1
            else:
                detectionState = DetectionState.Closed
                if self.score != 10:
                    self.score += 1



        return img, detectionState, self.score

    def show_window(self, img, detectionState, score):
        match detectionState:
            case DetectionState.Open:
                pred = 'Open'
            case DetectionState.Closed:
                pred = 'Closed'
            case DetectionState.Undetected:
                pred = 'Undetected'

        cv2.putText(img,
            pred,
            (50, 50),
            self.image_processing.font, 1,
            (0, 255, 255),
            2,
            cv2.LINE_4)

        cv2.putText(img,
            str(score),
            (50, 80),
            self.image_processing.font, 1,
            (0, 255 - score* 25.5, score* 25.5),
            2,
            cv2.LINE_4)

        cv2.imshow('Camera', img)
        cv2.waitKey(1)

    def detecting(self):
        self.detecting_state = True
        self.elapsed_time = time.time()

        while(self.detecting_state):
            if self.image_processing.camera.isOpened():
                img, detectionState, score = self.detect()
                if detectionState == DetectionState.Closed and self.detected_closed == False:
                    self.detected_closed = True
                    self.elapsed_time = time.time()
                if detectionState == DetectionState.Closed:
                    if time.time() - self.elapsed_time > 1.0:
                        winsound.Beep(3520, 500)
                else:
                    self.detected_closed = False
                self.show_window(img, detectionState, score)

        cv2.destroyAllWindows()
        #self.image_processing.destroy()

    def change_detecting_state(self):
        self.detecting_state = not self.detecting_state