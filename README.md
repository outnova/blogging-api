# 🚀 FastAPI Blogging Platform API

A robust and simple **RESTful API** built with **FastAPI** to manage blog posts. It features full **CRUD** (Create, Read, Update, Delete) capabilities, utilizing **SQLModel** for ORM and a **MySQL** database running in a **Docker** container for persistence.

---

## Prerequisites

Before starting, ensure you have the following installed on your system:

* **Python 3.8+**
* **Docker** and **Docker Compose** (for running the MySQL database)

## Getting Started

Follow these steps to set up and run the API locally.

### 1. Database Setup (MySQL via Docker)

This project relies on a local MySQL database. We'll use Docker to run it reliably.

1.  **Run the MySQL Container:** Execute the following command in your terminal. This command sets up a persistent MySQL 8.0 server and creates the initial database (`blog_db`).

    ```bash
    docker run --name fastapi-mysql-dev -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=blog_db -p 3306:3306 -v mysql_data:/var/lib/mysql -d mysql:8.0
    ```

2.  **Verify:** Ensure the container is running:
    ```bash
    docker ps
    ```

### 2. Python Environment Setup

1.  **Create a Virtual Environment:** It's best practice to isolate your project dependencies.
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the Environment:**
    * **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    * **Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

3.  **Install Dependencies:** Install all necessary libraries listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configure Environment Variables (`.env`)

You need to create a file named **`.env`** in the root directory of the project to securely manage your database credentials.

1.  **Create the file:** Touch or create the file named `.env`.
2.  **Add the following content:** (Use the exact credentials defined when running the Docker container).

    ```dotenv
    # Database Connection
    USER_DB=root
    PASSWORD_DB=yourpassword
    HOST_DB=localhost
    PORT_DB=3306
    NAME_DB=blog_db
    ```
    > **Note:** The API reads these variables to connect to the Docker container.

### 4. Run the Application

Start the FastAPI application using:

```bash
fastapi dev main.py
```

# 🚀 API para Plataforma de Blog en FastAPI

Una **API RESTful** robusta y sencilla construida con **FastAPI** para gestionar publicaciones de blog. Incluye funcionalidades completas de **CRUD** (Crear, Leer, Actualizar, Eliminar), utilizando **SQLModel** como ORM y una base de datos **MySQL** ejecutándose en un contenedor **Docker** para la persistencia de datos.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu sistema:

* **Python 3.8+**
* **Docker** (para ejecutar la base de datos MySQL)

## Puesta en Marcha

Sigue estos pasos para configurar y ejecutar la API localmente.

### 1. Configuración de la Base de Datos (MySQL vía Docker)

Este proyecto depende de una base de datos MySQL local. Usaremos Docker para ejecutarla de manera fiable.

1.  **Ejecutar el Contenedor MySQL:** Ejecuta el siguiente comando en tu terminal. Este comando configura un servidor MySQL 8.0 persistente y crea la base de datos inicial (`blog_db`).

    ```bash
    docker run --name fastapi-mysql-dev -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=blog_db -p 3306:3306 -v mysql_data:/var/lib/mysql -d mysql:8.0
    ```

2.  **Verificar:** Asegúrate de que el contenedor esté corriendo:
    ```bash
    docker ps
    ```

### 2. Configuración del Entorno Python

1.  **Crear un Entorno Virtual:** La mejor práctica es aislar las dependencias de tu proyecto.
    ```bash
    python3 -m venv .venv
    ```

2.  **Activar el Entorno:**
    * **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    * **Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

3.  **Instalar Dependencias:** Instala todas las librerías necesarias listadas en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configurar Variables de Entorno (`.env`)

Debes crear un archivo llamado **`.env`** en el directorio raíz del proyecto para gestionar de forma segura tus credenciales de la base de datos.

1.  **Crear el archivo:** Crea el archivo llamado `.env`.
2.  **Agregar el siguiente contenido:** (Usa las credenciales exactas definidas al ejecutar el contenedor Docker).

    ```dotenv
    # Conexión a la Base de Datos
    USER_DB=root
    PASSWORD_DB=yourpassword
    HOST_DB=localhost
    PORT_DB=3306
    NAME_DB=blog_db
    ```
    > **Nota:** La API lee estas variables para conectarse al contenedor Docker.

### 4. Ejecutar la Aplicación

Inicia la aplicación FastAPI usando su comando de desarrollo:

```bash
fastapi dev main.py