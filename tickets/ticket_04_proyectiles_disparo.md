# Ticket 04: Proyectiles y Sistema de Disparo (Listas y Memoria)

## 🎯 Objetivo
Haremos que nuestra nave pueda disparar proyectiles (balas) presionando la barra espaciadora. Aprenderemos a manejar múltiples objetos al mismo tiempo usando listas en Python y descubriremos la importancia de la **gestión de memoria** en los videojuegos.

---

## 📚 Conceptos Clave: Polimorfismo, Colecciones y Gestión de Memoria

### 🎭 Polimorfismo
El polimorfismo es la habilidad de tratar diferentes tipos de objetos de la misma manera si comparten una clase padre común.
En la clase `Game` tendremos una lista con *todos* los objetos activos en el juego (el jugador, las balas, los enemigos, etc.). El Bucle de Juego no necesita saber si un objeto es una nave o una bala: simplemente recorre la lista y llama a `.update(dt)` y `.draw(screen)` en cada uno de ellos. ¡Cada objeto sabe cómo comportarse!

### 🧹 Gestión de Memoria (Limpieza de Objetos)
Cuando disparas una bala, se crea un objeto en la memoria de la computadora. Si la bala sale de la parte superior de la pantalla y no la eliminamos, seguirá viajando hacia el espacio infinito para siempre.
Si juegas durante unos minutos, ¡podrías tener miles de balas invisibles consumiendo la memoria RAM y el procesador de tu computadora! Esto es lo que se conoce como una **Fuga de Memoria (Memory Leak)**. Para evitarlo, debemos destruir (eliminar de la lista) cualquier proyectil que salga de la pantalla.

### ⏱️ Temporizador de Enfriamiento (Cooldown)
Si permitimos que el jugador dispare una bala en cada fotograma, ¡disparará 60 balas por segundo! Para que el juego sea justo y equilibrado, implementaremos un temporizador que impida disparar otra bala hasta que haya pasado un cuarto de segundo (`0.25` segundos).

---

## 📋 Criterios de Aceptación
1. Se crea la clase `Bullet` en un nuevo archivo `src/projectiles.py` que hereda de `GameObject`.
2. Presionar la **Barra Espaciadora** dispara una bala desde la punta superior de la nave del jugador.
3. Las balas se mueven hacia arriba a una velocidad constante y rápida (por ejemplo, `600` píxeles por segundo).
4. El disparo tiene un enfriamiento de `0.25` segundos (máximo 4 disparos por segundo al mantener presionado).
5. Las balas que salgan de la pantalla por la parte superior se eliminan de la lista del juego.

---

## 🛠️ Detalles de Implementación Técnica

### Paso A: Crear la clase `Bullet` en `src/projectiles.py`
```python
import pygame
from src.base import GameObject

class Bullet(GameObject):
    def __init__(self, position: pygame.Vector2) -> None:
        # Creamos un rectángulo amarillo pequeño de 4x15 píxeles para representar la bala
        surface = pygame.Surface((4, 15))
        surface.fill((250, 204, 21)) # Amarillo brillante
        
        # Inicializamos el GameObject
        super().__init__(position, surface)
        # Las balas viajan hacia arriba, así que su velocidad vertical es negativa
        self.velocity = pygame.Vector2(0, -600.0)

    def update(self, dt: float) -> None:
        # Movemos la bala basada en su velocidad y el delta time
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Si la bala sale de la pantalla (su Y es menor a -50), la marcamos como "muerta"
        if self.position.y < -50:
            self.is_dead = True

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)
```

### Paso B: Modificar `PlayerShip` en `src/entities.py` para permitir disparos
```python
# Añade la importación al inicio de src/entities.py:
from src.projectiles import Bullet

# Modifica el __init__ de PlayerShip para agregar el temporizador de enfriamiento:
class PlayerShip(Ship):
    def __init__(self, position: pygame.Vector2) -> None:
        # ... código existente ...
        super().__init__(position, surface, health=3, speed=300.0)
        self.cooldown_timer = 0.0  # Temporizador inicial
        
    def update(self, dt: float) -> None:
        # Reducimos el temporizador con el tiempo transcurrido
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
            
        # ... código de movimiento existente (WASD / Flechas) ...
        # (Asegúrate de mantener el código de movimiento de la nave)
        
    def shoot(self) -> Bullet | None:
        # Si el temporizador llegó a 0, podemos disparar
        if self.cooldown_timer <= 0:
            self.cooldown_timer = 0.25 # Reiniciamos el enfriamiento a 0.25 segundos
            # La bala sale desde la parte de arriba de la nave (centro superior de su rectángulo)
            punta_nave = pygame.Vector2(self.rect.centerx, self.rect.top)
            return Bullet(punta_nave)
        return None
```

### Paso C: Modificar `src/main.py` para gestionar la lista de entidades
Actualizaremos la clase `Game` para manejar todas las entidades dinámicamente usando una **lista**:

```python
# En el __init__ de tu clase Game:
        # ... código anterior ...
        self.player = PlayerShip(pygame.Vector2(400, 500))
        
        # Lista que contendrá a todos los objetos activos en el juego
        self.entities: list = [self.player]

# En el método _handle_events de Game:
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                
        # Fuera del bucle de eventos, leemos si la barra espaciadora está presionada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            nueva_bala = self.player.shoot()
            if nueva_bala: # Si no estaba en cooldown y devolvió una bala
                self.entities.append(nueva_bala) # La añadimos a la lista de objetos activos

# En el método _update de Game:
    def _update(self, dt: float) -> None:
        # 1. Actualizamos todos los objetos de la lista (Polimorfismo en acción)
        for entity in self.entities:
            entity.update(dt)
            
        # 2. Filtramos la lista para quedarnos SOLO con los objetos que no estén "muertos"
        # Esto elimina automáticamente las balas fuera de la pantalla de la memoria
        self.entities = [e for e in self.entities if not e.is_dead]

# En el método _draw de Game:
    def _draw(self) -> None:
        self.screen.fill((15, 23, 42))
        
        # Dibujamos todos los objetos activos en pantalla
        for entity in self.entities:
            entity.draw(self.screen)
            
        pygame.display.flip()
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta el juego: `python src/main.py`
* [ ] Mantén presionada la barra espaciadora. ¿Las balas salen de forma constante y fluida en fila, en lugar de amontonarse en un solo bloque gigante?
* [ ] Para verificar la recolección de basura de memoria, añade temporalmente un `print(len(self.entities))` en el método `_update`. 
  - Comprueba que la cantidad de entidades aumenta cuando disparas y **vuelve a bajar exactamente a 1** cuando los proyectiles desaparecen por la parte superior de la pantalla. ¡No olvides quitar el `print` después de comprobarlo!
