# ¡Bienvenido al Curso de Introducción a la Programación con Pygame! 🚀

En este curso vamos a aprender a programar en **Python** creando un videojuego desde cero: un **Space Shooter clásico (juego de naves)** con movimiento, disparos, y una batalla contra un Jefe Final.

---

## 🛠️ Paso 1: Configurar nuestro entorno de desarrollo

Antes de escribir código, necesitamos preparar nuestra computadora. Sigue estos sencillos pasos:

1. **Instalar Python 3.12**:
   - Descarga e instala Python 3.12 desde [python.org](https://www.python.org/).
   - **IMPORTANTE**: Durante la instalación en Windows, marca la casilla que dice **"Add Python to PATH"** (Añadir Python al PATH) si todavía no lo has hecho.

2. **Crear una carpeta para el proyecto**:
   - Crea una carpeta en tu computadora llamada `mi-juego-pygame`.

3. **Crear un Entorno Virtual (Virtual Environment)**:
   - Los entornos virtuales evitan que las librerías de diferentes proyectos se mezclen y causen problemas.
   - Abre tu terminal (PowerShell en Windows o Terminal en macOS/Linux), navega a tu carpeta y escribe:
     ```bash
     python -m venv .venv
     ```
   - Si tu sistema tiene varias versiones de Python instaladas en Windows, puedes usar:
     ```powershell
     py -3.12 -m venv .venv
     ```
   - Activa el entorno virtual:
     - **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
     - **macOS/Linux**: `source .venv/bin/activate`

4. **Instalar Pygame**:
   - Pygame es la librería (caja de herramientas) que nos permitirá dibujar en pantalla, detectar teclas y reproducir sonidos.
   - Con el entorno virtual activado, escribe en tu terminal:
     ```bash
     pip install pygame
     ```

---

## 📚 Glosario de Conceptos de Programación

Durante este curso usaremos varios términos clave. Aquí tienes una explicación sencilla:

* **Variable**: Piensa en ella como una caja con una etiqueta donde guardas un dato (un número, texto o un color). Ejemplo: `velocidad = 5` o `nombre = "Nave"`
* **Función**: Un bloque de código con un nombre que realiza una tarea específica cuando lo llamas. Ejemplo: `dibujar_nave()`
* **Bucle (Loop)**: Código que se repite una y otra vez mientras se cumpla una condición. Nuestro juego usará un "Bucle de Juego" (`while True`) que se ejecuta 60 veces por segundo para actualizar la pantalla.
* **Condicional (`if`)**: Permite que el programa tome decisiones. "SI el jugador presiona la tecla Derecha, ENTONCES mueve la nave a la derecha".
* **Clase (Class) y Objeto (Object)**:
  - Una **Clase** es un plano o molde (como la receta para hacer galletas).
  - Un **Objeto** es la galleta real creada a partir de ese molde. Crearemos una clase `Ship` (Nave) y a partir de ella crearemos el objeto de nuestra propia nave.
* **Herencia (Inheritance)**: Permite que una clase herede características de otra. Por ejemplo, una clase `PlayerShip` (Nave del Jugador) y una clase `BossShip` (Nave del Jefe) pueden heredar cosas comunes de una clase base `Ship` (como tener vida y posición).

---

## 🗺️ Mapa de Ruta del Proyecto

El desarrollo se divide en 6 "tickets" o tareas secuenciales:

1. **Ticket 01**: Configurar la ventana y crear el Bucle de Juego básico.
2. **Ticket 02**: Crear la nave del jugador y aprender a dibujarla.
3. **Ticket 03**: Hacer que la nave se mueva con el teclado y no se salga de la pantalla.
4. **Ticket 04**: ¡Disparar proyectiles! Y aprender a borrarlos para no gastar memoria.
5. **Ticket 05**: Aparecer al Jefe Final, hacerlo moverse de lado a lado y detectar colisiones.
6. **Ticket 06**: Hacer que el Jefe nos dispare, añadir barras de vida y las pantallas de Victoria y Fin de Juego.

¡Adelante! Ve a la carpeta `tickets/` y abre el `ticket_01_configuracion_pantalla.md` para comenzar.
