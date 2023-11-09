# PLANTILLA DE APLICACIÓN INTAXLLIGENCE

Desplegar frondEnd utilizando Python como lenguaje que genere la vista.
Se crea una aplicación FLASK que se integra a la plataforma TTDA y llama servicios REST.

## Development and Deployemnt


### Cambios en configuración  

* El archivo de configuración se cambió a .env.json
* Este archivo se agregóa .gitignore
* El código para utilizar los ambientes se encuentra en utils.environemnt
* Para utilizarlo se deben ejecutar los siguientes pasos:
  1. En main.py cargar el archivo json utilizando la función loadEnvironment() (* sin error handling, el archivo debe existir y ser válido)
    > from utils.environment import loadEnvironment
    > loadEnvironment(".env.json")
  2. En cada lugar que se requiera una variable ambiente se debe usar la función getEnvironment que lee una llave del json
    > from utils.environment import getEnvironment
    > server = getEnvironment("RestServer")
* Se modificaron los siguientes archivos para utilizar estas funciones:
  * main.py
  * tokenlogin.py
  * tokenvalidation.py
  * restAPI.py
* Ya no es posible inyectar variables en las variables de ambiente, todo debe ser en el archivo JSON.
* Archivo .env.json de prueba:
    {
      "Server":{
      "ServerPort": ":443",
      "CertFile":"/usr/src/app/ssl/intaxlligence-crt",
      "KeyFile":"/usr/src/app/ssl/intaxlligence-key",
      "EnvMode":"DEV",
      "AppRoot":"/template",
      "SessionName":"TEMPLATE_DEV", 
      "Secret": "bNEve0R6zMBvErGjCJpJXo8I9wZxXh0C"
      },
      "DB2": {
      "Database": "SECURITY",
      "Hostname": "10.48.160.21",
      "DefaultSchema": "security",
      "User": "USER",
      "Password":"PASSWORD",
      "Port": "50000",
      "Security": "SSL",
      "Protocol": "TCPIP",
      "SSLServerCertificate": "/usr/src/app/ssl/db2cserver-arm"
      },
      "SecurityService": "https://localhost/appSecServ/getSessionInformation/",
      "RestServer": "localhost"
    }


  ### Ejemplo json Front ejecutar template 
  {
    "Server": {
        "EnvMode": "DEV",                            ---> Llave en la que se indica el modo de desarrollo en el que se cambia de accuerdo al ambiente en el que se desplega la solución
        "AppRoot": "/template",                      ---> Llave para indiicar la base url con la sera llamado el servicio
        "SessionName": "template",                   ---> Llave que connntiene el nombre que se le dará a la sesión.
        "Secret": "bNEve0R6zMBvErGjCJpJXo8I9wZxXh0C" ---> Llave que contiene el seccreto que será utilizada en la cookie del modulo desarrollado
      },
      "RestServerSec":"localhost",    ---> llave para conectar con los servicios de seguridad
      "ApiSecurity":"/appSecServ",    ---> llave api de los servicios de seguridad 
      "RestServer": "localhost",      ---> llave para conectar con los servicios del api del aplicativo
      "ApiService":"/templateApiGo",  ---> llave que hace referencia al api de los servicios del aplicativo
      "ApiDapm":"/dapmApi"            ---> llave para consumir un api diferente a los servicios de seguridad agregar
  } 

### Configuración Antigua

* Todas las variables de ambiente se guardan en el archivo .env
* Ejemplo de archivo .env con las variables mínimas requeridas:
  > ENV_MODE='DEV'
  > ENV_SECRET='<32 random characters>'
  > APP_ROOT='/template'
  > REST_SERVER='localhost'
  > SESSION_NAME='TEMPLATE_DEV'

* En UAT y PROD se sobreescriben las variables requeridas <https://vsupalov.com/docker-build-pass-environment-variables/>
  > docker build --build-arg var_name=${VARIABLE_NAME} (...)
* En los ambientes de desarrollo, UAT y producción tienen que estar las las siguientes varibles definidas al momento de ejecutar el forntEnd.
  * La variable  ENV_MODE en desarrollo es igual a DEV, en los ambientes de UAT y producción es PROD
    > ENV_MODE='DEV'
    > APP_ROOT='/template'
    > REST_SERVER='pro.eyttda.com'
  * El secreto se utiliza para encriptar la cookies de sesión.
    > ENV_SECRET=''
  * La variable ENV_SECRET de Flask está guardada en b64 y se puede generar con el siguiente comando:
    > python -c "import os; import base64; print(base64.b64encode(os.urandom(24)))"

### HTTPS

* La carpeta SSL contiene certificados de prueba.
  * "Llave de Prueba"
* Al liberar en UAT y PROD se usarán los certificados correspondientes.

### Desarrollo

* En desarrollo se puede ejecutat la aplicación con Flask o Gunicorn
  * Flask:
    > env ENV_MODE='DEV' REST_SERVER='localhost' python3 main.py
  * Gunicorn HTTPS usando certificados de prueba:
    > env ENV_MODE='DEV' gunicorn main:app --bind 0.0.0.0:443 --preload --certfile=ssl/server.crt --keyfile=ssl/server.key --workers 2
* En UAT y Prod sólo se usa Gunicorn llamado desde el container y con los certificados del ambiente
  * Probar construcción del container HTTPS usando certificados de prueba:
    > docker build . -t appname
    > docker run -d -p 443:443 --name appname appname
    > docker run -d -p 8470:443 --add-host=pro.eyttda.com:10.53.32.50 --name appname appname

### Routes/Views

* Deben estar en la carpeta view
* Cada ruta debe incluir el decorador token_valid
* No deben incluir el prefojo de URL, eso se agrega en main al iniciar la app

## LOG

  001. Create FLASK container(Docker)
  002. Add token validation functions
  003. Add HTML template
  004. Create action function, this function can idetifiy the form on the request.
  2020-06-05: Added default COREUI Dashboard

## Backlog

* Dockerfile: Incluir la ruta de los certificados
