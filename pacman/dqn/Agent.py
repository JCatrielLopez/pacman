import codecs
import json
import os
import random
import time
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.callbacks import TensorBoard
from keras.layers import Conv2D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import Adam


class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self._log_write_dir = self.log_dir
        self.writer = tf.summary.create_file_writer(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

    def _write_logs(self, logs, index):
        try:
            with self.writer.as_default():
                for name, value in logs.items():
                    tf.summary.scalar(name, value, step=index)
                    self.step += 1
                    self.writer.flush()
        except:
            pass


class DQNAgent:
    def __init__(self):

        self.action_space = 4
        self.lr = 0.05
        self.replay_memory_min = 25000
        self.batch_size = 100

        # Main model
        self.model = self.create_model()

        self.gamma = 0.99
        self.epsilon = 1
        self.epsilon_decay = 0.99
        self.min_epsilon = 0.001

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=50000)

        # Custom tensorboard object
        self.tensorboard = ModifiedTensorBoard(
            log_dir="logs/{}".format(int(time.time()))
        )

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0
        self.history = None

    def create_model(self):
        model = Sequential()

        model.add(Conv2D(16, 8, input_shape=(32, 32, 4)))
        model.add(Activation("relu"))
        model.add(Dropout(0.2))

        model.add(Conv2D(32, 4))
        model.add(Activation("relu"))
        model.add(Dropout(0.2))

        model.add(Flatten())

        model.add(Dense(64))

        model.add(Dense(self.action_space, activation="linear"))

        model.compile(
            loss="mse", optimizer=Adam(lr=self.lr), metrics=["accuracy"]
        )
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def train(self, terminal_state, step):
        if len(self.replay_memory) < self.replay_memory_min:
            return

        minibatch = random.sample(self.replay_memory, 64)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        for (
                index,
                (current_state, action, reward, new_current_state, done),
        ) in enumerate(minibatch):

            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.gamma * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        history = self.model.fit(
            np.array(X),
            np.array(y),
            validation_split=0.25,
            batch_size=self.batch_size,
            verbose=0,
            shuffle=False,
            callbacks=[self.tensorboard] if terminal_state else None,
        )

        self.history = self.appendHist(self.history, history.history)

        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > 10:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape))[0]

    def get_plot(self):
        if self.history is not None:
            plt.plot(self.history['accuracy'])
            plt.plot(self.history['val_accuracy'])
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()

            plt.plot(self.history['loss'])
            plt.plot(self.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()
        else:
            print("History None")

    def saveHist(self, path, history):
        with codecs.open(path, 'w', encoding='utf-8') as f:
            json.dump(history, f, separators=(',', ':'), sort_keys=True, indent=4)

    def loadHist(self, path):
        n = {}  # set history to empty
        if os.path.exists(path):  # reload history if it exists
            with codecs.open(path, 'r', encoding='utf-8') as f:
                n = json.loads(f.read())
        return n

    def appendHist(self, h1, h2):
        if h1 is None:
            return h2
        else:
            dest = {}
            for key, value in h1.items():
                dest[key] = value + h2[key]
            return dest
