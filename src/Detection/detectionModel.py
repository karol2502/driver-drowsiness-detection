import os
import torch


class DetectionModel:
    @staticmethod
    def load(model):
        dirname = os.path.dirname(__file__)
        model.load_state_dict(torch.load(os.path.join(dirname, 'Model/model_96.pt'), map_location=torch.device('cpu')))