import os
import warnings

# Suppress TF INFO & DEPRECATION messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error
warnings.filterwarnings('ignore', category=FutureWarning)  # ignore future warnings

import tensorflow_hub as hub

class YamnetModel:
    def __init__(self):
        self.model_handle = 'https://tfhub.dev/google/yamnet/1'
        self.model = hub.load(self.model_handle)
        self.class_map_path = self.model.class_map_path().numpy()

    def get_model(self):
        return self.model

    def get_class_map_path(self):
        return self.class_map_path


yamnet_instance = YamnetModel()   # Singleton
