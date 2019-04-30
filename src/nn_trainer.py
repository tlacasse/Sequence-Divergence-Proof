import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense

from exprmap import EXPRMAP, TERM_BOUND

# use a smaller training subset to "replicate" the lack of data in
# many other theorem proving domains.
TRAINING_TEST_SPLIT = 0.5
INPUT_NODES = TERM_BOUND * 2
HIDDEN_NODES = [6, 6, 6]
OUTPUT_NODES = TERM_BOUND * 2

x = np.load('data/nn_x.npy').astype('float64')
y = np.load('data/nn_y.npy').astype('float64')

# fit between 0 and 1
x[:] /= EXPRMAP.TERM_VALUE
y[:] /= EXPRMAP.TERM_VALUE

# shuffle for train and test split.
seed = random.randint(0, 100000)
np.random.seed(seed)
x = np.random.permutation(x)
np.random.seed(seed)
y = np.random.permutation(y)

# split into training and test
split_index = round(TRAINING_TEST_SPLIT * x.shape[0])
x_train = x[:split_index]
x_test  = x[split_index:]
y_train = y[:split_index]
y_test  = y[split_index:]

# model: INPUT_NODES - HIDDEN_NODES - OUTPUT_NODES 
model = Sequential()
model.add(Dense(HIDDEN_NODES[0], input_dim=INPUT_NODES, activation='relu'))
for h in HIDDEN_NODES[1:]:
    model.add(Dense(h, activation='relu'))
model.add(Dense(OUTPUT_NODES, activation='sigmoid'))

# train
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=40, batch_size=10) # better results with smaller batches

model.save('data/nn.h5')

# examples, to show accuracy

print()
print()
print()

vround = np.vectorize(round)

x = x_train[:10]
y = y_train[:10]
y_pred = model.predict(x)
y[:] *= 77
y_pred[:] *= 77
y_pred[:] = vround(y_pred[:])
print(y)
print(y_pred)
