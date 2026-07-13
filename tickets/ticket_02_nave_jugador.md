# Ticket 02: Creación de la Nave del Jugador (Entidades y Herencia)

## 🎯 Objetivo
Definiremos una estructura base para todos los objetos visuales de nuestro juego e implementaremos la clase para la nave del jugador. Este paso introduce uno de los conceptos más importantes de la programación: la **Herencia**.

---

## 📚 Concepto Clave: Herencia y Clases Abstractas

En un videojuego tendremos muchos objetos diferentes en pantalla: la nave del jugador, los disparos, los enemigos, el jefe final, etc. Todos ellos comparten cosas en común: tienen una posición, una imagen o dibujo, y necesitan actualizarse y dibujarse en cada fotograma.

Para no repetir el mismo código de posición y dibujo en cada objeto, usamos dos herramientas:
1. **Clase Abstracta (`GameObject`)**: Es como un plano muy general. Define que *cualquier* objeto del juego debe tener una posición y debe implementar obligatoriamente las funciones `update` (para actualizarse) y `draw` (para dibujarse). Usamos el módulo `abc` de Python para obligar a que esto se cumpla.
2. **Herencia (Inheritance)**:
   - `GameObject` (Clase Base) es el objeto genérico del juego.
   - `Ship` (Hereda de `GameObject`) es una versión especial que añade características de naves de combate (como vida y velocidad).
   - `PlayerShip` (Hereda de `Ship`) es la nave específica que controla el jugador con su propio diseño visual.

Al usar la palabra clave `super().__init__(...)`, le decimos a una clase hija que ejecute el constructor de su clase padre para configurar los datos básicos (como la posición).

---

## 📋 Criterios de Aceptación
1. Se define la clase abstracta `GameObject` en un nuevo archivo `src/base.py` con los métodos obligatorios `update` y `draw`.
2. Se crea la clase `Ship` en `src/entities.py` que hereda de `GameObject`.
3. Se crea la clase `PlayerShip` en `src/entities.py` que hereda de `Ship`.
4. La nave del jugador (`PlayerShip`) aparece al inicio en el centro-inferior de la pantalla: coordenadas `(400, 500)`.
5. La nave se dibuja en pantalla (por ejemplo, dibujando un triángulo azul brillante).
6. El bucle del juego (`Game`) actualiza y dibuja la nave en cada fotograma.

---

## 🛠️ Detalles de Implementación Técnica

### Paso A: Crear la Clase Base en `src/base.py`
Este archivo contendrá el molde genérico para cualquier objeto del juego:

```python
from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    def __init__(self, position: pygame.Vector2, sprite: pygame.Surface) -> None:
        # Guardamos la posición como un Vector2 (X, Y) para operaciones matemáticas limpias
        self.position = position
        
        # El sprite es la imagen o superficie visual del objeto
        self.sprite = sprite
        
        # El rect representa el rectángulo contenedor para posicionar y detectar colisiones
        self.rect = sprite.get_rect(center=(position.x, position.y))
        
        # Atributo que nos servirá más adelante para saber si el objeto debe eliminarse
        self.is_dead = False

    @abstractmethod
    def update(self, dt: float) -> None:
        # Cada objeto tendrá que decidir cómo se mueve o actualiza cada fotograma
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        # Cada objeto decidirá cómo se dibuja en la pantalla
        pass
```

### Paso B: Crear las Naves en `src/entities.py`
Heredamos de `GameObject` para crear nuestras naves de combate:

```python
import pygame
from src.base import GameObject

class Ship(GameObject):
    def __init__(self, position: pygame.Vector2, sprite: pygame.Surface, health: int, speed: float) -> None:
        # Llamamos al constructor de GameObject
        super().__init__(position, sprite)
        self.health = health
        self.max_health = health
        self.speed = speed

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health <= 0:
            self.is_dead = True


class PlayerShip(Ship):
    def __init__(self, position: pygame.Vector2) -> None:
        # Creamos una superficie transparente de 40x40 píxeles para dibujar nuestra nave
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Dibujamos un triángulo azul cielo sobre esa superficie
        # Puntos del triángulo: arriba-centro (20, 0), abajo-izquierda (0, 40), abajo-derecha (40, 40)
        pygame.draw.polygon(surface, (56, 189, 248), [(20, 0), (0, 40), (40, 40)])
        
        # Inicializamos la nave del jugador con 3 de vida y velocidad de 300 píxeles por segundo
        super().__init__(position, surface, health=3, speed=300.0)

    def update(self, dt: float) -> None:
        # Por ahora la nave no se mueve sola
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # Dibujamos el sprite en la posición que indica su rectángulo contenedor
        screen.blit(self.sprite, self.rect)
```

### Paso C: Integrar la Nave en `src/main.py`
Modificamos nuestra clase `Game` para incluir la nave:

```python
# Añade la importación al inicio de src/main.py:
from src.entities import PlayerShip

# En el __init__ de tu clase Game:
        # ... código anterior ...
        self.is_running = True
        
        # Creamos la nave del jugador en la posición inicial (400, 500)
        self.player = PlayerShip(pygame.Vector2(400, 500))

# En el método _update:
    def _update(self, dt: float) -> None:
        # Actualizamos el estado de la nave
        self.player.update(dt)

# En el método _draw:
    def _draw(self) -> None:
        self.screen.fill((15, 23, 42))
        
        # Dibujamos la nave del jugador en la pantalla
        self.player.draw(self.screen)
        
        pygame.display.flip()
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta el juego: `python src/main.py`
* [ ] Confirma que se abre la ventana azul y aparece un triángulo azul brillante centrado en la parte inferior.
* [ ] Verifica que no hay errores ni excepciones en la terminal.
