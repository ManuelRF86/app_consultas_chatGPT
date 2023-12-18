import pytest
import os
import requests


def test_home_route():
    response = requests.get('http://localhost:5000/')
    assert response.status_code == 200

def test_analizar_documento_route():
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, 'data')
    ruta = os.path.join(data_dir, 'Viggo_Peter_Mortensen_grande.txt')
    
    with open(ruta, 'rb') as archivo:
        data = {'archivo': archivo, 'nombre': 'John', 'pregunta': '¿Qué edad tiene nuestro amigo Viggo?'}
        response = requests.post('http://localhost:5000/analizar_documento', files=data)
        
    assert response.status_code == 200

def test_consultas_route():
    response = requests.get('http://localhost:5000/consultas')
    assert response.status_code == 200

def test_realizar_consulta_route():
    response = requests.get('http://localhost:5000/realizar_consulta?nombre=Anuel')
    assert response.status_code == 200