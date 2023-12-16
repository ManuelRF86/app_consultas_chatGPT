from flask import Flask, request, render_template
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import sqlite3
from datetime import datetime
import pymysql


app = Flask(__name__)

#langchain
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

#AWS
username = "admin"
password = "12345678"
host = "gpt-database.cjlljwohiugl.eu-north-1.rds.amazonaws.com" 
port = 3306

def insertar_registro(fecha_hora, nombre, pregunta, respuesta):
    conn = sqlite3.connect('data/GPT_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO GPT_database (Registro, Nombre, Consulta, Respuesta) VALUES (?, ?, ?, ?)',
                   (fecha_hora, nombre, pregunta, respuesta))
    conn.commit()
    conn.close()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analizar_documento', methods=['POST'])
def analizar_documento():
    if 'archivo' in request.files:
        archivo = request.files['archivo']
        if not archivo:
            return "Error: Ningún archivo introducido"
                
        nombre = request.form.get('nombre')  # Obtener el nombre del formulario
        if not nombre:
            return "Error: Debe introducir su nombre"
        
        pregunta = request.form.get('pregunta')
        if not pregunta:
            return "Error: La pregunta no se proporcionó"

        # Leer el archivo en fragmentos de 4KB
        fragment_size = 4096
        while True:
            parte = archivo.read(fragment_size)
            if not parte:
                break

            try:
                response = qa_document_chain.run(
                    input_document=parte.decode('latin-1'),
                    question=pregunta,
                )

                # Obtener la fecha y hora actual
                fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insertar en la base de datos
                insertar_registro(fecha_hora_actual, nombre, pregunta, str(response))

                # Procesar la respuesta si es necesario
                return str(response)    
            except Exception as e:
                return f"Error: {str(e)}"

        

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
