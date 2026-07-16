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