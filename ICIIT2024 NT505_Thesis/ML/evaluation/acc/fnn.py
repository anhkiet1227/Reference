from tensorflow.keras.layers import Dense
from sklearn import svm
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

df = pd.read_csv('output_with_labels.csv')
labels = df['Label']
token_ids = df['Token IDs'].apply(eval)  # Assuming token IDs are stored as strings of lists

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Pad sequences for LSTM input
max_length = max(len(tokens) for tokens in token_ids)
padded_token_ids = pad_sequences(token_ids, maxlen=max_length, padding='post')

# Split the data
X_train, X_test, y_train, y_test = train_test_split(padded_token_ids, encoded_labels, test_size=0.2, random_state=42)


# Create the FNN model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(max_length,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

# save the model
model.save('../bin/fnn.h5')

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5).astype('int32')  # Convert probabilities to binary predictions

# Calculate accuracy
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(f"Precision: {precision_score(y_test, y_pred) * 100:.2f}%")
print(f"Recall: {recall_score(y_test, y_pred) * 100:.2f}%")
print(f"F1: {f1_score(y_test, y_pred) * 100:.2f}%")