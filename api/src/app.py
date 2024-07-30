import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Gallery
import cloudinary
import cloudinary.uploader

load_dotenv()

path = os.path.abspath(os.path.join('../api/', os.path.dirname(__name__)))

app = Flask(__name__, instance_relative_config=False, instance_path=path)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db)
CORS(app)

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('API_KEY'),
    api_secret = os.getenv('API_SECRET'),
    secure=True
)


@app.route('/')
def main():
    return jsonify({ "status": "Server running successfully"})

@app.route('/api/gallery', methods=['GET'])
def obtener_galeria():

    images = Gallery.query.all()
    images = [image.serialize() for image in images]

    return jsonify(images), 200


@app.route('/api/upload', methods=['POST'])
def upload_image():
    
    if not 'title' in request.form:
        return jsonify({ "msg": "El titulo es requerido"}), 400 
    
    if not 'image' in request.files:
        return jsonify({ "msg": "La imagen es requerida"}), 400 

    # Capturar los datos a guardar
    title = request.form['title']
    image = request.files['image']

    # Upload de la imagen a cloudinary
    resp = cloudinary.uploader.upload(image, folder="gallery_ft25")

    # si no fue cargada correctamente envio mensaje de error
    if not 'secure_url' in resp:
        return jsonify({ "error": "No se pudo subir la imagen"}), 400
    
    # Guardamos la imagen en la base de datos
    gallery = Gallery(title=title, image=resp['secure_url'], public_id=resp['public_id'])
    gallery.save()

    # Si fue guardada correctamente devolvemos la informacion
    if gallery:
        return jsonify(gallery.serialize()), 200
    
    return jsonify({ "error": "No se pudo guardar la imagen"}), 400

@app.route('/api/update-image/<int:id>', methods=['PUT'])
def update_image(id):
    
    if not 'title' in request.form:
        return jsonify({ "msg": "El titulo es requerido"}), 400 
    
    if not 'image' in request.files:
        return jsonify({ "msg": "La imagen es requerida"}), 400 

    # Capturar los datos a guardar
    title = request.form['title']
    image = request.files['image']

    gallery = Gallery.query.filter_by(id=id).first()
    if not gallery:   
        return jsonify({ "msg": "La imagen que quiere eliminar no existe"}), 400
    

    # Upload de la imagen a cloudinary
    resp = cloudinary.uploader.upload(image, public_id=gallery.public_id, overwrite=True)

    # si no fue cargada correctamente envio mensaje de error
    if not 'secure_url' in resp:
        return jsonify({ "error": "No se pudo subir la imagen"}), 400
    
    # Guardamos la imagen en la base de datos
    gallery.title = title
    gallery.image = resp['secure_url']
    gallery.update()

    # Si fue guardada correctamente devolvemos la informacion
    if gallery:
        return jsonify(gallery.serialize()), 200
    
    return jsonify({ "error": "No se pudo guardar la imagen"}), 400


@app.route('/api/remove-image/<int:id>', methods=['DELETE'])
def remove_image(id):

    gallery = Gallery.query.filter_by(id=id).first()

    if not gallery:
        return jsonify({ "msg": "La imagen que quiere eliminar no existe"}), 400
    

    resp = cloudinary.uploader.destroy(gallery.public_id)
    if not 'result' in resp:
        return jsonify({ "msg": "No se pudo eliminar la imagen"}), 400
    
    gallery.delete()

    return jsonify({ "success": "Imagen eliminada correctamente"}), 200


if __name__ == '__main__':
    app.run()