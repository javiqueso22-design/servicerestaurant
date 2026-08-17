from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import math

app = Flask(__name__)
CORS(app)

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/cercanos', methods=['GET'])
def buscar_cercanos():
    try:
        lat_usuario = float(request.args.get('lat'))
        lon_usuario = float(request.args.get('lon'))
        limite = int(request.args.get('limite', 3))
        cadena = request.args.get('cadena', 'TODAS') # Recibe qué restaurante busca
        
        with open('restaurantes.json', 'r', encoding='utf-8') as file:
            restaurantes = json.load(file)
            
        # Filtrar por cadena si el usuario no eligió "TODAS"
        if cadena != 'TODAS':
            restaurantes = [r for r in restaurantes if r['cadena'] == cadena]
                
        for r in restaurantes:
            dist = calcular_distancia(lat_usuario, lon_usuario, r['lat'], r['lon'])
            r['distancia_km'] = round(dist, 2)
            
        restaurantes_ordenados = sorted(restaurantes, key=lambda x: x['distancia_km'])
        return jsonify(restaurantes_ordenados[:limite])
        
    except Exception as e:
        return jsonify({"error": "Parámetros inválidos."}), 400

@app.route('/todos', methods=['GET'])
def obtener_todos():
    try:
        with open('restaurantes.json', 'r', encoding='utf-8') as file:
            restaurantes = json.load(file)
        return jsonify(restaurantes)
    except Exception as e:
        return jsonify({"error": "Error cargando la base de datos."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)