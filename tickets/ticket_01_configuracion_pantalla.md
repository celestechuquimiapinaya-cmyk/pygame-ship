# Ticket 01: Configuración de la Ventana y Bucle de Juego Principal

## 🎯 Objetivo
El objetivo de esta primera tarea es crear la ventana de nuestro juego y establecer el "Bucle de Juego" (Game Loop) básico. Utilizaremos la Programación Orientada a Objetos (POO) para organizar nuestro código dentro de una clase llamada `Game`.

---

## 📚 Concepto Clave: Encapsulación y el Ciclo de Vida del Juego

En lugar de escribir todo nuestro código suelto en un archivo largo, usaremos una **Clase**. Imagina que una clase es una "caja templada" que agrupa datos (variables) y acciones (funciones/métodos). A esto lo llamamos **Encapsulación**.

El ciclo de vida de un juego tiene tres fases que se ejecutan una y otra vez (normalmente 60 veces por segundo):
1. **Inicialización (`__init__`)**: Preparamos la ventana, el reloj y las variables iniciales. Esto ocurre solo una vez al principio.
2. **Ejecución (`run`)**: Es el bucle principal. Mientras el juego esté activo (`is_running = True`), repetirá tres sub-tareas:
   - **Manejar Eventos (`_handle_events`)**: Escucha qué hace el usuario (por ejemplo, si presiona una tecla o hace clic en la "X" para cerrar la ventana).
   - **Actualizar Estado (`_update`)**: Calcula posiciones, movimientos, vidas y físicas.
   - **Dibujar (`_draw`)**: Dibuja todo en la pantalla limpia y muestra el nuevo fotograma.
3. **Cierre**: Detiene Pygame de forma limpia cuando salimos del bucle.

### ¿Qué es el Delta Time (`dt`)?
Las computadoras rápidas ejecutan código más rápido que las lentas. Si hiciéramos que una nave se mueva 5 píxeles por fotograma, en una computadora muy rápida iría a toda velocidad y en una lenta iría muy despacio.
Para solucionar esto usamos **Delta Time (`dt`)**, que es el tiempo real (en segundos) que pasó entre el fotograma anterior y el actual (aproximadamente `0.016` segundos a 60 FPS). Al multiplicar nuestros movimientos por `dt`, aseguramos que la nave se mueva a la misma velocidad física en cualquier computadora.

---

## 📋 Criterios de Aceptación
1. Al ejecutar el archivo principal, se abre una ventana de tamaño `800x600` píxeles con el título **"Retro Space Shooter"**.
2. El juego mantiene una tasa de FPS estable limitada a `60` fotogramas por segundo.
3. El juego calcula y rastrea el Delta Time (`dt`) en segundos.
4. Presionar el botón 'X' de la ventana cierra el juego inmediatamente sin congelarse ni mostrar errores en la terminal.
5. El fondo de la pantalla se pinta de un color azul oscuro moderno (por ejemplo, `#0F172A`) en cada fotograma.

---

## 🛠️ Detalles de Implementación Técnica

Crea un archivo llamado `src/main.py` y escribe la estructura básica de la clase `Game`:

```python
import sys
import pygame

class Game:
    def __init__(self) -> None:
        # Inicializa todos los módulos de Pygame
        pygame.init()
        
        # Crea la ventana de 800 de ancho por 600 de alto
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Retro Space Shooter")
        
        # El reloj nos ayuda a controlar los FPS (fotogramas por segundo)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self) -> None:
        # Este es el Bucle de Juego principal
        while self.is_running:
            # tick(60) limita el juego a 60 FPS y devuelve el tiempo en milisegundos.
            # Lo dividimos por 1000.0 para convertirlo a segundos (Delta Time).
            dt = self.clock.tick(60) / 1000.0
            
            # Pasos del bucle:
            self._handle_events()  # 1. Escuchar al usuario
            self._update(dt)       # 2. Actualizar las físicas/posiciones
            self._draw()           # 3. Dibujar la pantalla
            
        # Cuando el bucle termina, cerramos Pygame limpiamente
        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        # Revisamos todos los eventos que ocurrieron
        for event in pygame.event.get():
            # Si el usuario hace clic en cerrar la ventana (la 'X')
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self, dt: float) -> None:
        # Por ahora no actualizamos nada, esto se llenará en los siguientes tickets
        pass

    def _draw(self) -> None:
        # Limpiamos la pantalla con un color azul pizarra oscuro (#0F172A)
        # En RGB, este color es (15, 23, 42)
        self.screen.fill((15, 23, 42))
        
        # pygame.display.flip() actualiza toda la pantalla con lo que acabamos de dibujar
        pygame.display.flip()

# Este bloque asegura que el juego solo comience si ejecutamos este archivo directamente
if __name__ == "__main__":
    game = Game()
    game.run()
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta tu código en la terminal: `python src/main.py`
* [ ] Confirma que aparece una ventana titulada "Retro Space Shooter".
* [ ] Verifica que el fondo de la ventana es azul oscuro.
* [ ] Haz clic en el botón de cerrar ('X') y comprueba que la ventana se cierra de inmediato y la terminal vuelve a estar libre sin mostrar mensajes de error.
