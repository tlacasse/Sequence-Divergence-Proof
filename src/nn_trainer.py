import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense, Dropout

from exprmap import EXPRMAP, TERM_BOUND

# use a smaller training subset to "replicate" the lack of data in
# many other theorem proving domains.
TRAINING_TEST_SPLIT = 0.1
INPUT_NODES = TERM_BOUND * 2
HIDDEN_NODES = 6
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
model.add(Dense(HIDDEN_NODES, input_dim=INPUT_NODES, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(OUTPUT_NODES, activation='sigmoid'))

# train
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=20, batch_size=50)

# results
print(model.evaluate(x_train, model.predict(x_train)))
print(model.evaluate(x_test, model.predict(x_test)))

model.save('data/nn.h5')
