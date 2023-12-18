# Proyecto de base de datos con AWS RDS, Flask y OpenAI

Este proyecto fue desarrollado por un equipo de cuatro estudiantes de Data Science, compuesto por Steven Noboa, María Neches, Manuel Reina y Águeda González. El objetivo principal de la aplicación es conectar una base de datos SQL alojada en AWS con Langchaim de OpenAI utilizando Flask (python).

### Descripción del proyecto
La aplicación permite a los usuarios subir archivos en formato de texto plano (.txt), scripts de Python (.py) y cuadernos Jupyter (.ipynb). Estos archivos se procesan utilizando la tecnología Langchaim de OpenAI para realizar tareas como resúmenes automáticos o incluso generar chistes basados en el contenido de los archivos.

La información relevante se almacena en una base de datos SQL en AWS:

+ Nombre de la persona que hace la solicitud.
+ Fecha y hora del registro.
+ Consulta realizada (contenido del archivo).
+ Respuesta generada por OpenAI.
+ Nombre del archivo introducido.
Además, la aplicación ofrece la funcionalidad de consultar todos los registros almacenados en la base de datos, permitiendo filtrarlos por el nombre de la persona que hizo la solicitud.

### Requisitos previos
Antes de comenzar con la aplicación, habrá que tener instalados:

+ Docker: Para facilitar la implementación y ejecución de la aplicación.
+ Python y pip: Necesarios para ejecutar scripts y pruebas.

### Configuración del proyecto
Clona el repositorio:
```
git clone https://github.com/ManuelRF86/app_consultas_chatGPT.git
```
Accede al directorio del proyecto:
```
cd app_consultas_chatGPT
```

### Ejecución de la aplicación
Construye la imagen de Docker:
```
docker build -t manuelreina/app_aws:v2 .
```
Ejecuta el contenedor Docker:

```
docker run -p 5000:5000 manuelreina/app_aws:v2
```

La aplicación estará accesible en http://localhost:5000