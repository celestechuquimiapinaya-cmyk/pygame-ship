# Ticket 03: Sistemas de Control y Movimiento (Vectores y Teclado)

## 🎯 Objetivo
Haremos que nuestra nave espacial responda al teclado del jugador (teclas de flechas o letras WASD) para que pueda moverse por la pantalla. Además, nos aseguraremos de que la nave no pueda salirse de los límites de la ventana del juego.

---

## 📚 Conceptos Clave: Vectores, Normalización y Límites

### 🧭 Vectores en 2D
En programación de videojuegos, las posiciones y movimientos se representan mediante **Vectores en 2D** (`pygame.Vector2`). Un vector es simplemente un par de números `(x, y)`:
- `x` indica la posición horizontal (izquierda a derecha).
- `y` indica la posición vertical (arriba a abajo).
*Nota: En Pygame, el punto (0,0) está arriba a la izquierda. Si aumentamos X nos movemos a la derecha; si aumentamos Y nos movemos hacia abajo.*

### 📐 ¿Por qué normalizar un Vector?
Si presionamos la flecha Derecha, nuestra dirección es `(1, 0)`. Si presionamos Arriba, es `(0, -1)`.
¿Pero qué pasa si presionamos ambas a la vez? Nuestra dirección sería `(1, -1)`. Si aplicamos matemáticas básicas (el teorema de Pitágoras), la velocidad en diagonal sería aproximadamente `1.41`, ¡lo que significa que la nave se movería un 41% más rápido en diagonal que en línea recta!
Para solucionar este error tan común en los videojuegos, **normalizamos** el vector. Normalizar significa ajustar su tamaño (longitud) para que siempre valga exactamente `1`, sin importar en qué dirección esté apuntando.

### 🛡️ Restricción de Bordes (Clamping)
Para evitar que el jugador se mueva infinitamente y desaparezca de la pantalla, debemos limitar las coordenadas de la nave. Usaremos una función muy útil de Pygame que ajusta automáticamente los límites de un rectángulo contenedor para mantenerlo dentro de otro (la pantalla del juego).

---

## 📋 Criterios de Aceptación
1. Presionar las flechas de dirección (Izquierda/Derecha/Arriba/Abajo) o las teclas **W/A/S/D** mueve la nave en esa dirección.
2. El movimiento es independiente del frame rate: la nave se mueve a una velocidad constante escalada por el Delta Time (`dt`).
3. La nave no puede salirse de la ventana visible de `800x600`. Si llega al borde, se detiene inmediatamente.

---

## 🛠️ Detalles de Implementación Técnica

### Paso A: Modificar el método `update` en `src/entities.py`
Vamos a actualizar la clase `PlayerShip` para que lea las teclas presionadas y calcule el movimiento:

```python
    def update(self, dt: float) -> None:
        # 1. Obtener una lista de todas las teclas presionadas
        keys = pygame.key.get_pressed()
        
        # 2. Crear un vector de dirección inicializado en cero
        direction = pygame.Vector2(0, 0)
        
        # 3. Detectar movimiento horizontal (Izquierda / Derecha)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
            
        # 4. Detectar movimiento vertical (Arriba / Abajo)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
            
        # 5. Normalizar la dirección si nos estamos moviendo (longitud > 0)
        if direction.length() > 0:
            direction = direction.normalize()
            
        # 6. Actualizar la posición de la nave basada en: dirección * velocidad * delta_time
        self.position += direction * self.speed * dt
        
        # 7. Sincronizar el rectángulo del sprite con la nueva posición física
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # 8. Limitar la nave para que no salga de la pantalla (800x600)
        pantalla_limite = pygame.Rect(0, 0, 800, 600)
        # clamp_ip restringe "in-place" (sobre sí mismo) el rectángulo dentro del rectángulo de la pantalla
        self.rect.clamp_ip(pantalla_limite)
        
        # Sincronizamos de vuelta nuestra posición con el rectángulo ajustado
        self.position.xy = self.rect.center
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta el juego: `python src/main.py`
* [ ] Presiona las flechas y las letras WASD. ¿La nave se mueve correctamente en las 8 direcciones?
* [ ] Intenta moverte en diagonal. ¿Se siente fluido y a la misma velocidad que el movimiento recto?
* [ ] Conduce la nave hacia las cuatro esquinas de la ventana. ¿La nave se detiene perfectamente en los bordes sin salirse ni un solo píxel?
