from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from tensorflow.keras.models import load_model
from make_model_mobilenet import (
    SparseCategoricalAccuracy,
    SparseCategoricalPrecision,
    SparseCategoricalRecall,
    SparseCategoricalAUC
)



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Ajoute ceci juste après app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle .keras
MODEL_PATH = "mobilenetv2_best.keras"

custom_objects = {
    "SparseCategoricalAccuracy": SparseCategoricalAccuracy,
    "SparseCategoricalPrecision": SparseCategoricalPrecision,
    "SparseCategoricalRecall": SparseCategoricalRecall,
    "SparseCategoricalAUC": SparseCategoricalAUC,
}

model = load_model(MODEL_PATH, custom_objects=custom_objects)

# Liste des classes (à adapter selon ton problème)
# class_names = ['class1', 'class2', 'class3']  # Remplace par tes vraies classes
class_names1 = [
    "n02113712-miniature_poodle",
    "n02089973-English_foxhound",
    "n02115913-dhole",
    "n02090379-redbone",
    "n02085782-Japanese_spaniel",
    "n02088632-bluetick",
    "n02111500-Great_Pyrenees",
    "n02089078-black-and-tan_coonhound",
    "n02088364-beagle",
    "n02089867-Walker_hound",
    "n02113624-toy_poodle",
    "n02115641-dingo",
    "n02086079-Pekinese",
    "n02112018-Pomeranian",
    "n02088238-basset",
    "n02113023-Pembroke",
    "n02086240-Shih-Tzu",
    "n02086646-Blenheim_spaniel",
    "n02113186-Cardigan",
    "n02086910-papillon",
    "n02087394-Rhodesian_ridgeback",
    "n02113799-standard_poodle",
    "n02090622-borzoi",
    "n02088466-bloodhound",
    "n02111277-Newfoundland",
    "n02085936-Maltese_dog",
    "n02112706-Brabancon_griffon",
    "n02111889-Samoyed",
    "n02112350-keeshond",
    "n02085620-Chihuahua",
    "n02116738-African_hunting_dog",
    "n02087046-toy_terrier",
    "n02112137-chow",
    "n02113978-Mexican_hairless",
    "n02088094-Afghan_hound",
    "n02090721-Irish_wolfhound"
]



class_names = ['Chihuahua',
 'Japanese_spaniel',
 'Maltese_dog',
 'Pekinese',
 'Tzu',
 'Blenheim_spaniel',
 'papillon',
 'toy_terrier',
 'Rhodesian_ridgeback',
 'Afghan_hound',
 'basset',
 'beagle',
 'bloodhound',
 'bluetick',
 'tan_coonhound',
 'Walker_hound',
 'English_foxhound',
 'redbone',
 'borzoi',
 'Irish_wolfhound',
 'Newfoundland',
 'Great_Pyrenees',
 'Samoyed',
 'Pomeranian',
 'chow',
 'keeshond',
 'Brabancon_griffon',
 'Pembroke',
 'Cardigan',
 'toy_poodle',
 'miniature_poodle',
 'standard_poodle',
 'Mexican_hairless',
 'dingo',
 'dhole',
 'African_hunting_dog']


# Fonction de prétraitement
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((128, 128))  # adapte selon l'input shape de ton modèle
    image = np.array(image) / 255.0   # normalise
    image = np.expand_dims(image, axis=0)  # ajoute dimension batch
    return image

# Endpoint pour prédire à partir d'une image
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = preprocess_image(contents)
        prediction = model.predict(img)
        predicted_class = class_names[np.argmax(prediction[0])]
        confidence = float(np.max(prediction[0]))
        return {"class": predicted_class, "confidence": confidence}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
