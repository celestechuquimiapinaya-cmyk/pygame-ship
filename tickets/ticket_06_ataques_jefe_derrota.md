# Ticket 06: Ataques del Jefe, Vida y Derrota (Máquinas de Estado)

## 🎯 Objetivo
Haremos que la batalla contra el jefe sea un reto real: el jefe disparará proyectiles hacia abajo a intervalos regulares, añadiremos una barra de salud a nuestra nave y gestionaremos el estado de **Derrota (Game Over)** si el jefe nos destruye antes.

---

## 📚 Conceptos Clave: Máquina de Estados y Transformación Gráfica

### 🚦 Máquina de Estados del Juego
Un juego no siempre se actualiza y dibuja igual. Al principio del desarrollo solo teníamos la pantalla de juego principal. En el ticket anterior añadimos la pantalla de Victoria. Ahora añadiremos la pantalla de Derrota (Game Over).
Este flujo se organiza mediante una **Máquina de Estados** muy simple:
- Estado **JUGANDO**: Se mueven las naves, se detectan colisiones, se puede disparar.
- Estado **VICTORIA**: Se detiene la acción y se muestra un mensaje de felicitación.
- Estado **GAME OVER**: Se detiene la acción y se muestra un mensaje de derrota.

Controlamos esto usando variables booleanas o estados de texto para decidir qué dibujar y qué actualizar en cada fotograma.

### 🔄 Inversión Gráfica (Flipping)
La nave del jefe usa un triángulo dibujado. En el ticket anterior, dibujamos un triángulo con la punta apuntando hacia abajo, lo cual funciona bien. Pero si estuviéramos usando imágenes (Sprites), Pygame nos permite girar o voltear una imagen horizontal o verticalmente de forma sencilla usando `pygame.transform.flip(...)`. Aprenderemos a usarlo para asegurar que la nave del jefe apunte en la dirección correcta.

---

## 📋 Criterios de Aceptación
1. En el constructor del jefe, se invierte verticalmente su superficie visual para simular que apunta hacia abajo.
2. Se crea la clase `BossBullet` en `src/projectiles.py` que hereda de `GameObject`. Es un rectángulo rojo pequeño que viaja hacia abajo a `300` píxeles por segundo.
3. El jefe dispara una `BossBullet` automáticamente cada `1.5` segundos.
4. El jugador tiene una barra de salud pequeña dibujada encima de su nave (ancho 40, alto 5), que se encoge cuando recibe daño.
5. Cuando una bala del jefe choca con el jugador:
   - La bala se destruye (`is_dead = True`).
   - El jugador recibe 1 punto de daño.
6. Si la vida del jugador llega a 0, la nave del jugador se destruye (desaparece) y el juego pasa a un estado de **"GAME OVER"** mostrando un texto rojo gigante centrado.

---

## 🛠️ Detalles de Implementación Técnica

### Paso A: Crear la clase `BossBullet` en `src/projectiles.py`
Añade esta clase al archivo:

```python
class BossBullet(GameObject):
    def __init__(self, position: pygame.Vector2) -> None:
        # Bala del jefe: rectángulo rojo vertical de 4x15 píxeles
        surface = pygame.Surface((4, 15))
        surface.fill((239, 68, 68)) # Rojo brillante
        
        super().__init__(position, surface)
        # Viaja hacia abajo (Y positivo)
        self.velocity = pygame.Vector2(0, 300.0)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Se destruye si sale por la parte inferior de la pantalla (600)
        if self.position.y > 650:
            self.is_dead = True

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)
```

### Paso B: Modificar `BossShip` en `src/entities.py` para voltear sprite y disparar
Modifica la clase `BossShip`:

```python
# Importa la bala del jefe al inicio del archivo:
from src.projectiles import BossBullet

class BossShip(Ship):
    def __init__(self, position: pygame.Vector2) -> None:
        # ... código de creación de superficie existente ...
        pygame.draw.polygon(surface, (239, 68, 68), [(0, 0), (80, 0), (40, 80)])
        
        # Volteamos verticalmente el sprite (primer booleano: voltear X=Falso, segundo: voltear Y=Verdadero)
        surface_invertida = pygame.transform.flip(surface, False, True)
        
        super().__init__(position, surface_invertida, health=20, speed=150.0)
        self.velocity = pygame.Vector2(self.speed, 0)
        
        # Temporizador para controlar cuándo dispara el jefe
        self.shoot_cooldown = 1.5

    def update(self, dt: float) -> None:
        # ... código de movimiento existente ...
        
        # Reducir el temporizador del disparo
        self.shoot_cooldown -= dt
        
    def shoot(self) -> BossBullet | None:
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 1.5 # Dispara cada 1.5 segundos
            # La bala sale desde el centro inferior de su rectángulo
            base_jefe = pygame.Vector2(self.rect.centerx, self.rect.bottom)
            return BossBullet(base_jefe)
        return None
        
    # (Asegúrate de conservar el método draw() con su barra de vida)
```

### Paso C: Dibujar la barra de vida del Jugador en `PlayerShip` (en `src/entities.py`)
Modifica el método `draw` de `PlayerShip`:

```python
    def draw(self, screen: pygame.Surface) -> None:
        # 1. Dibujamos la nave del jugador
        screen.blit(self.sprite, self.rect)
        
        # 2. Dibujamos la barra de vida sobre la nave del jugador (solo si sigue vivo)
        if not self.is_dead:
            bar_width = 40
            bar_height = 5
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 10
            
            # Fondo rojo oscuro
            pygame.draw.rect(screen, (153, 27, 27), (bar_x, bar_y, bar_width, bar_height))
            # Barra verde brillante proporcional a la vida
            porcentaje_vida = self.health / self.max_health
            green_width = int(bar_width * max(0.0, porcentaje_vida))
            pygame.draw.rect(screen, (34, 197, 94), (bar_x, bar_y, green_width, bar_height))
```

### Paso D: Actualizar el bucle en `src/main.py`
Gestionamos las balas del jefe, el daño al jugador y el estado de "Game Over":

```python
# En el __init__ de tu clase Game:
        # ... código anterior ...
        self.game_won = False
        self.game_over = False  # Nuevo estado de derrota

# En el método _update de Game:
    def _update(self, dt: float) -> None:
        # Si ganamos o perdimos, no actualizamos la lógica del juego
        if self.game_won or self.game_over:
            return
            
        # 1. Control del spawn del jefe
        if self.boss is None and not self.player.is_dead:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.boss = BossShip(pygame.Vector2(400, 80))
                self.entities.append(self.boss)
                
        # 2. Hacer que el jefe dispare
        if self.boss:
            nueva_bala_jefe = self.boss.shoot()
            if nueva_bala_jefe:
                self.entities.append(nueva_bala_jefe)

        # 3. Actualizar todas las entidades
        for entity in self.entities:
            entity.update(dt)
            
        # 4. Colisiones de balas del jugador contra el Jefe
        if self.boss:
            balas_jugador = [e for e in self.entities if isinstance(e, Bullet)]
            for bala in balas_jugador:
                if bala.rect.colliderect(self.boss.rect):
                    self.boss.take_damage(1)
                    bala.is_dead = True
                    
            if self.boss.is_dead:
                self.game_won = True
                self.entities.remove(self.boss)
                self.boss = None
                
        # 5. Colisiones de balas del Jefe contra el Jugador
        if not self.player.is_dead:
            balas_jefe = [e for e in self.entities if isinstance(e, BossBullet)]
            for bala in balas_jefe:
                if bala.rect.colliderect(self.player.rect):
                    self.player.take_damage(1)
                    bala.is_dead = True
                    
            if self.player.is_dead:
                self.game_over = True
                self.entities.remove(self.player)

        # 6. Limpieza de entidades muertas
        self.entities = [e for e in self.entities if not e.is_dead]

# En el método _draw de Game:
    def _draw(self) -> None:
        self.screen.fill((15, 23, 42))
        
        # Dibujamos las entidades si siguen activas
        for entity in self.entities:
            entity.draw(self.screen)
            
        # Dibujar pantalla de Victoria
        if self.game_won:
            fuente = pygame.font.SysFont("Arial", 64, bold=True)
            texto = fuente.render("¡VICTORIA!", True, (34, 197, 94))
            rect_texto = texto.get_rect(center=(400, 300))
            self.screen.blit(texto, rect_texto)
            
        # Dibujar pantalla de Game Over (Derrota)
        elif self.game_over:
            fuente = pygame.font.SysFont("Arial", 64, bold=True)
            texto = fuente.render("GAME OVER", True, (239, 68, 68))
            rect_texto = texto.get_rect(center=(400, 300))
            self.screen.blit(texto, rect_texto)
            
        pygame.display.flip()
```

---

## 🧪 Lista de Verificación para Pruebas (Checklist)
* [ ] Ejecuta el juego. Espera a que aparezca el jefe. ¿La punta del triángulo del jefe ahora apunta hacia abajo (hacia ti)?
* [ ] Observa al jefe. ¿Dispara proyectiles rojos que viajan hacia abajo en tu dirección cada 1.5 segundos?
* [ ] Verifica que tu nave azul tiene una barra de vida verde pequeña encima.
* [ ] Déjate golpear por un proyectil rojo del jefe. ¿El proyectil desaparece y tu barra de salud disminuye?
* [ ] Deja que tu barra de vida baje a cero. ¿Tu nave desaparece y aparece la pantalla roja gigante "GAME OVER"?
