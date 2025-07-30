# src/make_model_mobilenet.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


# ----------------------------- #
#    Custom Metrics Classes     #
# ----------------------------- #

class SparseCategoricalAccuracy(tf.keras.metrics.Metric):
    def __init__(self, name='Accuracy', **kwargs):
        super().__init__(name=name, **kwargs)
        self.accuracy = tf.keras.metrics.Accuracy()

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.squeeze(y_true, axis=-1) if len(y_true.shape) > 1 else y_true
        y_pred_classes = tf.argmax(y_pred, axis=-1)
        self.accuracy.update_state(y_true, y_pred_classes, sample_weight)

    def result(self):
        return self.accuracy.result()

    def reset_state(self):
        self.accuracy.reset_state()


class SparseCategoricalPrecision(tf.keras.metrics.Metric):
    def __init__(self, name='Precision', **kwargs):
        super().__init__(name=name, **kwargs)
        self.precision = tf.keras.metrics.Precision()

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.squeeze(y_true, axis=-1) if len(y_true.shape) > 1 else y_true
        y_pred_classes = tf.argmax(y_pred, axis=-1)
        self.precision.update_state(y_true, y_pred_classes, sample_weight)

    def result(self):
        return self.precision.result()

    def reset_state(self):
        self.precision.reset_state()


class SparseCategoricalRecall(tf.keras.metrics.Metric):
    def __init__(self, name='Recall', **kwargs):
        super().__init__(name=name, **kwargs)
        self.recall = tf.keras.metrics.Recall()

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.squeeze(y_true, axis=-1) if len(y_true.shape) > 1 else y_true
        y_pred_classes = tf.argmax(y_pred, axis=-1)
        self.recall.update_state(y_true, y_pred_classes, sample_weight)

    def result(self):
        return self.recall.result()

    def reset_state(self):
        self.recall.reset_state()


class SparseCategoricalAUC(tf.keras.metrics.Metric):
    def __init__(self, name='AUC', **kwargs):
        super().__init__(name=name, **kwargs)
        self.auc = tf.keras.metrics.AUC(multi_label=True)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = tf.squeeze(y_true, axis=-1) if len(y_true.shape) > 1 else y_true
        y_true_one_hot = tf.one_hot(tf.cast(y_true, tf.int32), depth=tf.shape(y_pred)[-1])
        self.auc.update_state(y_true_one_hot, y_pred, sample_weight)

    def result(self):
        return self.auc.result()

    def reset_state(self):
        self.auc.reset_state()


# ----------------------------- #
#      Build & Compile Model    #
# ----------------------------- #

def create_mobilenetv2_model(input_shape, num_classes, learning_rate):
    """
    Crée et compile un modèle MobileNetV2 avec des métriques personnalisées.
    """
    base_model = MobileNetV2(input_shape=input_shape, include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(512, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss=SparseCategoricalCrossentropy(),
        metrics=[
            SparseCategoricalAccuracy(),
            SparseCategoricalPrecision(),
            SparseCategoricalRecall(),
            SparseCategoricalCrossentropy(name='log_loss'),
            SparseCategoricalAUC()
        ]
    )

    return model


def prepare_labels_for_mobilenetv2(labels):
    """
    Prépare les labels au format integer (si one-hot).
    """
    if len(labels.shape) > 1 and labels.shape[-1] > 1:
        labels = np.argmax(labels, axis=-1)
    return labels.astype(np.int32)


# ----------------------------- #
#         Train Model           #
# ----------------------------- #

def train_mobilenetv2_model(model, x_train, y_train, x_val, y_val, epochs, patience):
    """
    Entraîne le modèle MobileNetV2 avec EarlyStopping.
    """
    y_train = prepare_labels_for_mobilenetv2(y_train)
    y_val = prepare_labels_for_mobilenetv2(y_val)

    early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)

    history = model.fit(
        x_train, y_train,
        epochs=epochs,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping]
    )

    return history


# ----------------------------- #
#         Test Model            #
# ----------------------------- #

def test_mobilenetv2_model(model, x_test, y_test, class_names):
    """
    Teste le modèle image par image et retourne les prédictions.
    """
    y_test = prepare_labels_for_mobilenetv2(y_test)
    results = []
    y_pred_proba = []

    for idx, image in enumerate(x_test):
        image_batch = np.expand_dims(image, axis=0)
        prediction = model.predict(image_batch, verbose=0)
        pred_index = np.argmax(prediction[0])
        true_index = y_test[idx]

        results.append((class_names[pred_index], class_names[true_index]))
        y_pred_proba.append(prediction[0])

    return results, np.array(y_pred_proba)