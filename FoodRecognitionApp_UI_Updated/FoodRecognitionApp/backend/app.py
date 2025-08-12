from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = load_model('indian_food_model.h5')
class_names = ['butter_chicken', 'biryani', 'masala_dosa', 'palak_paneer', 'samosa']

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img_path = 'temp.jpg'
    file.save(img_path)

    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img) / 255.0
    img_tensor = np.expand_dims(img_tensor, axis=0)

    prediction = model.predict(img_tensor)
    class_index = np.argmax(prediction[0])
    food_name = class_names[class_index]

    food_data = {
        'butter_chicken': {
            'summary': 'Creamy tomato-based curry with grilled chicken pieces.',
            'ingredients': ['Chicken', 'Tomatoes', 'Cream', 'Butter', 'Spices']
        },
        'biryani': {
            'summary': 'Aromatic rice dish cooked with meat or vegetables and spices.',
            'ingredients': ['Basmati Rice', 'Meat', 'Yogurt', 'Saffron', 'Spices']
        },
        'masala_dosa': {
            'summary': 'Crispy South Indian crepe filled with spiced potato filling.',
            'ingredients': ['Rice', 'Urad Dal', 'Potatoes', 'Spices', 'Coconut Chutney']
        },
        'palak_paneer': {
            'summary': 'Paneer cubes in creamy spinach gravy.',
            'ingredients': ['Spinach', 'Paneer', 'Cream', 'Garlic', 'Spices']
        },
        'samosa': {
            'summary': 'Deep-fried pastry with spicy potato filling.',
            'ingredients': ['Potatoes', 'Peas', 'Flour', 'Cumin', 'Chili']
        }
    }

    info = food_data.get(food_name, {'summary': 'No info available', 'ingredients': []})

    return jsonify({
        'name': food_name.replace('_', ' ').title(),
        'summary': info['summary'],
        'ingredients': info['ingredients']
    })

if __name__ == '__main__':
    app.run(debug=True)
