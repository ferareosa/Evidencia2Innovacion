# Evidencia de Aprendizaje N° 2

**Análisis y Diseño del Sistema ABMC de Contactos**

**Autor:** [Luis Alberto Lagger - Fernando Areosa]  
**Asignatura:** Innovación y Gestión de Datos  
**Profesores:** [Carlos Charletti - Ramiro Adrián Ceballes]  
**Fecha de Entrega:** Hasta el 17 de septiembre de 2025

---

## Instalador

[Click aqui para descargar](https://drive.google.com/file/d/1B06Xxp0Ywgqoo7_n9pbPmN_Z2dLpdUyl/view?usp=sharing)

## Índice

1. [Modelo de Clases](#1-modelo-de-clases)
2. [Modelo de Datos](#2-modelo-de-datos)
3. [Investigación Teórica](#3-investigación-teórica)
   - [3.1. Programación Orientada a Objetos (POO)](#31-programación-orientada-a-objetos-poo)
   - [3.2. Sentencias SQL (DDL, DML, DCL)](#32-sentencias-sql-ddl-dml-dcl)
   - [3.3. Proceso de Conexión a SQLite en Python](#33-proceso-de-conexión-a-sqlite-en-python)

---

## 1. Modelo de Clases

El diseño del sistema se basa en el paradigma de la Programación Orientada a Objetos (POO), que permite estructurar el código de manera modular y reutilizable. El proyecto está organizado en diferentes clases y módulos para separar responsabilidades y facilitar su mantenimiento.

El modelo de clases principal incluye:

- **Clase Contacto** (en _models.py_): Esta clase es la plantilla que modela un contacto individual. Sus atributos son las propiedades que describen a un contacto, como el nombre, el apellido, el teléfono y el email.
- **Clase Database** (en _database.py_): Esta clase encapsula toda la lógica para el almacenamiento y la recuperación de los datos. Se encarga de gestionar la conexión con la base de datos SQLite y de ejecutar todas las consultas SQL. Esto es un claro ejemplo de encapsulamiento, ya que la complejidad de la gestión de la base de datos queda oculta del resto del programa.
- **Clase App** (en _gui.py_): Esta clase representa la Interfaz Gráfica de Usuario (GUI). Actúa como el puente entre el usuario y la clase Database. Al interactuar con la interfaz (por ejemplo, al hacer clic en un botón), la clase App llama a los métodos de la clase Database sin necesidad de conocer los detalles de las sentencias SQL que se ejecutan internamente.

A continuación, se presenta un diagrama simple que ilustra la relación entre las clases principales del sistema:



classDiagram

    class App {
      - root
      - db
      - formulario
      - tree
      + __init__()
      + on_closing()
      + actualizar()
      + eliminar()
    }

    class Database {
      - db_name
      - conn
      - cursor
      + conectar()
      + crear_tabla()
      + insertar()
      + listar()
      + modificar()
      + eliminar()
      + buscar()
      + cerrar()
    }

    class Contacto {
      - id
      - nombre
      - apellido
      - telefono
      - email
      + __init__()
      + __str__()
    }

    App --> Database : usa
    App --> Contacto : manipula
    Database ..> Contacto : persiste

### Explicación del Diagrama:

- **App → Database**: La clase _App_ (la interfaz de usuario gui) utiliza una instancia de la clase _Database_ para interactuar con la base de datos. En el código, esto se muestra en la línea `self.db = Database()`. Esta relación se conoce como **agregación**.
- **Database → Contacto**: La clase _Database_ manipula objetos de la clase _Contacto_. Por ejemplo, cuando se inserta un contacto, se le pasa un objeto _Contacto_ a la base de datos para que lo guarde. Esto también es una **relación de dependencia**.

En resumen, la clase _App_ no necesita saber cómo se guardan los datos, solo le pide a _Database_ que lo haga. A su vez, _Database_ se encarga de convertir la información del objeto _Contacto_ en una sentencia SQL para la base de datos. Esta es una excelente demostración de cómo el **encapsulamiento y la modularidad** de la POO funcionan en la práctica.

---

## 2. Modelo de Datos

Para la persistencia de los datos, el sistema utiliza una base de datos relacional SQLite. El modelo de datos consiste en una única tabla llamada **Contactos**, la cual almacena la información de cada contacto.

### Estructura de la tabla:

| Campo    | Tipo de Dato | Restricciones             | Descripción                                                          |
| -------- | ------------ | ------------------------- | -------------------------------------------------------------------- |
| id       | INTEGER      | PRIMARY KEY AUTOINCREMENT | Identificador único del contacto. Se genera automáticamente.         |
| nombre   | TEXT         | NOT NULL                  | Nombre del contacto. No puede ser nulo.                              |
| apellido | TEXT         | NOT NULL                  | Apellido del contacto. No puede ser nulo.                            |
| telefono | TEXT         | NOT NULL                  | Número de teléfono del contacto.                                     |
| email    | TEXT         | NOT NULL UNIQUE           | Dirección de correo electrónico. Debe ser única y no puede ser nula. |

---

## 3. Investigación Teórica

### 3.1. Programación Orientada a Objetos (POO)

La POO es un paradigma de programación que utiliza **objetos** para modelar el mundo real, organizando el código en torno a datos y comportamientos.

- **Clases**: Una clase es una plantilla o plano para crear objetos. Ejemplo: la clase _Contacto_ define los atributos (_nombre, apellido, teléfono, email_) y el constructor (`__init__`).
- **Objetos**: Una instancia concreta de una clase. Ejemplo: un nuevo contacto creado con datos como `nombre="Juan"`, `email="juan@ejemplo.com"`.
- **Atributos**: Propiedades que describen a un objeto (en _Contacto_: `id, nombre, apellido, telefono, email`).
- **Métodos**: Acciones que los objetos pueden realizar. Ejemplo: en _Database_, el método `insertar_contacto()` guarda un nuevo contacto en la base de datos.

---

### 3.2. Sentencias SQL (DDL, DML, DCL)

Las sentencias SQL se clasifican según su propósito:

- **DDL (Lenguaje de Definición de Datos):** define la estructura de la base.
  - `CREATE TABLE`: crea la tabla _Contactos_ si no existe (método `crear_tabla`).
- **DML (Lenguaje de Manipulación de Datos):** manipula datos en las tablas.
  - `INSERT`: Alta de contacto (`insertar_contacto`).
  - `SELECT`: Consulta de contactos (`listar_contactos`, `buscar_contacto`).
  - `UPDATE`: Modificación de contacto (`modificar_contacto`).
  - `DELETE`: Baja de contacto (`eliminar_contacto`).
- **DCL (Lenguaje de Control de Datos):** gestiona permisos (`GRANT`, `REVOKE`). No se usan en el código, pero son clave en entornos multiusuario.

---

### 3.3. Proceso de Conexión a SQLite en Python

La conexión a la base de datos se maneja en la clase _Database_ con el módulo estándar `sqlite3`.

1. **Conexión**: `sqlite3.connect()` abre la base o la crea si no existe.
2. **Cursor**: `conn.cursor()` permite ejecutar comandos SQL.
3. **Ejecución**: `cursor.execute()` ejecuta sentencias SQL (con `?` para prevenir inyección).
4. **Confirmación**: `conn.commit()` guarda los cambios permanentemente.
5. **Cierre**: `conn.close()` libera recursos al salir (se ejecuta en `on_closing` en _gui.py_).
