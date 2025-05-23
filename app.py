import tensorflow as tf
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np
from numpy.linalg import norm
import os
from tqdm import tqdm
import pickle


# Load pre-trained ResNet50 model
model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

# Add GlobalMaxPooling2D layer on top of ResNet50
model = tf.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

# Print model summary
print(model.summary())

# Function to extract features from an image
def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

# List of image file paths
filenames = []

for file in os.listdir('images'):
    filenames.append(os.path.join('images',file))

# List to store extracted features
feature_list = []

# Extract features for each image
for file in tqdm(filenames):
   feature_list.append(extract_features(file, model))

# Convert feature list to numpy array
feature_array = np.array(feature_list)

# Print shape of the feature array
print(feature_array.shape)

pickle.dump(feature_list,open('embedding.pkl','wb'))
pickle.dump(filenames,open('filenames.pkl','wb'))




