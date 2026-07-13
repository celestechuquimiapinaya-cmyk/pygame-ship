# Ticket 05: Aparición del Jefe y Colisiones (Físicas y Sobrescritura)

## 🎯 Objetivo
Introduciremos al Jefe Final del juego. Haremos que aparezca en la parte superior de la pantalla y se mueva horizontalmente de lado a lado. Además, implementaremos la física de **colisión** para que nuestras balas puedan golpearlo, bajarle vida y derrotarlo para ganar el juego.

---

## 📚 Conceptos Clave: Sobrescritura de Métodos y Detección de Colisiones

### ✍️ Sobrescritura de Métodos (Method Overriding)
El jefe es una nave, así que heredará de la clase `Ship`. Sin embargo, el jefe no se mueve como el jugador (no usa teclado) ni se dibuja igual. 
Para resolver esto, usaremos la **Sobrescritura**. Esto significa que definiremos los métodos `update` y `draw` dentro de `BossShip`. Aunque se llamen igual que en la clase base, reemplazarán su comportamiento por defecto por las reglas específicas del jefe: moverse de lado a lado y dibujar una barra de salud encima de su cabeza.

### 💥 Detección de Colisiones con Rectángulos
En muchos videojuegos en 2D, las colisiones no se calculan pixel por pixel (ya que sería extremadamente lento). En su lugar, aproximamos los objetos a rectángulos invisibles que los rodean, llamados **Hitboxes**.
Pygame tiene una función maravillosa llamada `colliderect`. Si el rectángulo de una bala se cruza en el espacio con el rectángulo del jefe, `rect1.colliderect(rect2)` devolverá `True`. ¡Así de fácil detectamos un impacto!

---

## 📋 Criterios de Aceptación
1. Se crea la clase `BossShip` en `src/entities.py` heredando de `Ship`. Tiene un tamaño grande (80x80 píxeles) y 20 puntos de vida (HP).
2. El jefe aparece en la parte superior central de la pantalla después de transcurrir 5 segundos de juego.
3. El jefe se mueve de lado a lado horizontalmente. Al tocar el borde izquierdo o derecho de la pantalla, invierte su dirección de movimiento.
4. Cuando una bala del jugador golpea al jefe:
   - La bala se marca como muerta (`is_dead = True`) y desaparece del juego.
   - El jefe recibe 1 punto de daño.
5. El jefe dibuja una barra de salud visual sobre él (un fondo rojo estático y una barra verde encima que se encoge según la vida que le quede).
6. Al llegar a 0 de vida, el jefe muere y la pantalla muestra un texto centrado de **"¡VICTORIA!"**.

---

## 🛠️ Detalles de Implementación Técnica

### Paso A: Crear la clase `BossShip` en `src/entities.py`
Añade esta clase al final del archivo:

```python
class BossShip(Ship):
    def __init__(self, position: pygame.Vector2) -> None:
        # Creamos una superficie de 80x80 para el jefe
        surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        # Dibujamos un triángulo morado/rojo grande apuntando hacia abajo
        pygame.draw.polygon(surface, (239, 68, 68), [(0, 0), (80, 0), (40, 80)])
        
        # Inicializamos con 20 de vida y velocidad de 150 píxeles por segundo
        super().__init__(position, surface, health=20, speed=150.0)
        
        # El jefe tiene una velocidad horizontal inicial
        self.velocity = pygame.Vector2(self.speed, 0)

    def update(self, dt: float) -> None:
        # Movemos al jefe horizontalmente
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Si toca el borde derecho (800) o izquierdo (0), rebotamos invirtiendo la velocidad X
        if self.rect.right >= 800:
            self.rect.right = 800
            self.velocity.x *= -1
            self.position.x = self.rect.centerx
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.velocity.x *= -1
            self.position.x = self.rect.centerx

    def draw(self, screen: pygame.Surface) -> None:
        # 1. Dibujamos el triángulo del jefe
        screen.blit(self.sprite, self.rect)
        
        # 2. Dibujamos la barra de vida sobre él
        bar_width = 80
        bar_height = 8
        # Posición de la barra: centrada horizontalmente y 15 píxeles arriba del jefe
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        
        # Fondo de la barra (Rojo oscuro/apagado)
        pygame.draw.rect(screen, (153, 27, 27), (bar_x, bar_y, bar_width, bar_height))
        
        # Frente de la barra (Verde brillante) escalado por el porcentaje de vida restante
        porcentaje_vida = self.health / self.max_health
        green_width = int(bar_width * porcentaje_vida)
        pygame.draw.rect(screen, (34, 197, 94), (bar_x, bar_y, green_width, bar_height))
```

### Paso B: Integrar el spawn del Jefe y colisiones en `src/main.py`
Modificamos `Game` para gestionar el tiempo de spawn, colisiones y la victoria:

```python
# En el __init__ de tu clase Game:
        # ... código anterior ...
        self.entities: list = [self.player]
        
        # Variables de control del Jefe
        self.boss = None
        self.spawn_timer = 5.0 # Tiempo en segundos para que aparezca el jefe
        self.game_won = False

# En el método _update de Game:
    def _update(self, dt: float) -> None:
        if self.game_won:
            return  # Si ya ganamos, detenemos el juego
            
        # 1. Gestionar el temporizador del jefe si no ha aparecido
        if self.boss is None:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.boss = BossShip(pygame.Vector2(400, 80)) # Aparece en el centro-alto
                self.entities.append(self.boss)
                
        # 2. Actualizar todas las entidades
        for entity in self.entities:
            entity.update(dt)
            
        # 3. Detectar colisiones entre balas del jugador y el Jefe
        if self.boss:
            # Filtramos para conseguir solo las balas activas en la lista
            balas = [e for e in self.entities if isinstance(e, Bullet)]
            for bala in balas:
                # Comprobamos colisión rectangular
                if bala.rect.colliderect(self.boss.rect):
                    self.boss.take_damage(1) # El jefe recibe daño
                    bala.is_dead = True       # La bala se destruye
                    
            # Comprobar si el jefe ha sido derrotado
            if self.boss.is_dead:
                self.game_won = True
                self.entities.remove(self.boss)
                self.boss = None

        # 4. Filtrar y eliminar objetos destruidos de la lista
        self.entities = [e for e in self.entities if not e.is_dead]

# En el método _draw de Game:
    def _draw(self) -> None:
        self.screen.fill((15, 23, 42))
        
        # Dibujamos las entidades
        for entity in self.entities:
            entity.draw(self.screen)
            
        # Si ganamos, dibujamos el texto de victoria en el centro
        if self.game_won:
            fuente = pygame.font.SysFont("Arial", 64, bold=True)
            texto = fuente.render("¡VICTORIA!", True, (34, 197, 94))
            # Centramos el texto en la pantalla
            rect_texto = texto.get_rect(center=(400, 300))
            self.screen.blit(texto, rect_texto)
            
        pygame.display.flip()
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta el juego. Espera 5 segundos sin disparar. ¿El triángulo grande del Jefe aparece en la parte superior?
* [ ] Observa al Jefe. ¿Se desplaza de izquierda a derecha y rebota suavemente al tocar los bordes de la pantalla?
* [ ] Dispara al Jefe. ¿Las balas desaparecen al tocarlo y la barra de salud verde sobre su cabeza se reduce?
* [ ] Sigue disparando hasta que su salud llegue a cero. ¿El jefe desaparece y aparece el texto verde gigante "¡VICTORIA!" en el centro de la pantalla?
