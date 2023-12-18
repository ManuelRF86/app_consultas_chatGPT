from flask import Flask, request, render_template
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from datetime import datetime
import pymysql
from key import *

app = Flask(__name__)

#AWS
username = "admin"
password = AWS_password
host = "gpt-database.cjlljwohiugl.eu-north-1.rds.amazonaws.com" 
port = 3306
database="gpt_database"

def insertar_registro(fecha_hora, nombre,nombre_archivo, pregunta, respuesta):
    
    conn = pymysql.connect(host = host,
                     user = username,
                     port=port,
                     password = password,
                     database=database
                     )

    cursor = conn.cursor()
    cursor.execute('INSERT INTO gpt_table (Registro, Nombre, Archivo, Consulta, Respuesta) VALUES (%s, %s, %s, %s, %s)',
                   (fecha_hora, nombre,nombre_archivo, pregunta, respuesta))
    conn.commit()
    conn.close()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analizar_documento', methods=['POST'])
def analizar_documento():

    openai_api_key = request.form.get("api_key")

    if openai_api_key:
        
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
        qa_chain = load_qa_chain(llm, chain_type="map_reduce")
        qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain) 

    else:
        openai_api_key= openai_key_private
    
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
        qa_chain = load_qa_chain(llm, chain_type="map_reduce")
        qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
    

    if 'archivo' in request.files:
        archivo = request.files['archivo']
        if not archivo:
            return "Error: Ningún archivo introducido"
                
        nombre = request.form.get('nombre')
        if not nombre:
            return "Error: Debe introducir su nombre"
        
        pregunta = request.form.get('pregunta')
        if not pregunta:
            return "Error: La pregunta no se proporcionó"
        
        tipos_aceptados = {'.txt', '.py', '.ipynb'}

        if archivo.filename and not any(archivo.filename.lower().endswith(ext) for ext in tipos_aceptados):
            error_message = "Error: Tipo de archivo no admitido"
            return render_template('index.html', error_message=error_message)

        # leer el archivo en fragmentos de 4KB
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

                fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                insertar_registro(fecha_hora_actual, nombre,archivo.filename, pregunta, str(response))

                return render_template('respuestas.html', pregunta=pregunta, respuesta=str(response))
            except Exception as e:
                return render_template('respuestas.html', pregunta=pregunta, respuesta=str(e))

@app.route('/consultas')
def consultas():
    
    return render_template('consultas.html')

@app.route('/realizar_consulta', methods=['GET'])
def realizar_consulta():
    nombre = request.args.get('nombre')

    conn = pymysql.connect(
        host=host,
        user=username,
        port=port,
        password=password,
        database=database
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        if nombre:
            consulta = f"SELECT * FROM gpt_table WHERE nombre LIKE LOWER('%{nombre}%')"
        else:
            consulta = "SELECT * FROM gpt_table"

        cursor.execute(consulta)
        resultados = cursor.fetchall()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {str(e)}")
        resultados = []

    finally:
        cursor.close()
        conn.close()

    return render_template('results_BBDD.html', resultados=resultados)      

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')