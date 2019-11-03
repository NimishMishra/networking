import keras
from keras.models import Sequential, load_model
from keras.layers import Dense



model = Sequential()
model.add(Dense(10, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(50, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(10, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
model.add(Dense(23,activation='softmax'))

model = keras.models.load_model("best_model.model")