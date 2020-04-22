import os
from ..models import Pet, Type, Gender
from collections import OrderedDict

import tensorflow as tf

import pandas as pd
import numpy as np

class PredictService:
    def __init__(self):
        self.model_path = os.environ.get("MODEL_PATH", '/model/model.h5')
        if os.path.exists(self.model_path) and os.path.isfile(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
            self.ready = True
        else:
            print("No model to predict")
            self.ready = False

    def predict(self, pet: Pet):
        if self.ready:
            pet_to_test = OrderedDict(Type= 1 if pet.animal_type == Type.DOG else 2,
                Age= pet.age,
                Breed1 = pet.breed1.id,
                Breed2 = pet.breed2.id if pet.breed2 is not None else 0,
                Gender =  0 if pet.gender == Gender.MALE else 0,
                Color1 = pet.color1.id,
                Color2 = pet.color2.id if pet.color2 is not None else 0,
                Color3 = pet.color3.id if pet.color3 is not None else 0,
                MaturitySize = pet.maturity_size,
                FurLength = pet.fur_length,
                Vaccinated = pet.vaccinated,
                Dewormed = pet.dewormed,
                Sterilized = pet.sterilized,
                Health = pet.health,
                Fee = pet.fee)
            pet_to_test = pd.DataFrame(pet_to_test, index = [0])
            test = np.array(pet_to_test, dtype=np.float)
            test = tf.keras.utils.normalize(
                test, axis=-1, order=1
            )
            return int(np.argmax(self.model.predict(test), axis=-1)[0])