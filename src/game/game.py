import pygame
import time
from src.utils.settings import WINDOW_SIZE, FPS, GRID_SIZE
from src.game.snake import Snake
from src.game.food import Food
from src.utils.input_handler import InputHandler
from src.ui.renderer import Renderer
from src.game.game_state import GameState
from src.ui.game_stats import GameStats

class Game:
    def __init__(self, start_with_ai=False, ai_algorithm="astar", speed=10):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.snake = Snake()
        self.food = Food()
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)
        self.game_state = GameState()
        
        # Game flow control
        self.is_running = True
        self.is_playing = True  # Set to True for human mode to start immediately
        self.current_speed = speed  # Use the passed speed parameter
        self.is_paused = False
        self.last_update_time = time.time()
        
        # Set initial control mode and AI algorithm
        if start_with_ai:
            self.input_handler.current_ai_name = ai_algorithm
            self.input_handler.set_control_type("ai")
            
            # Create stats window for AI mode with callbacks
            self.stats_window = GameStats(
                self.input_handler.get_current_ai_name(),
                speed_callback=self.on_speed_change,
                pause_callback=self.on_pause_toggle
            )
        else:
            self.input_handler.set_control_type("human")  # Explicitly set human control
            self.stats_window = None

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.game_state.reset()
        self.last_update_time = time.time()
        if self.stats_window:
            self.stats_window.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                    return
                
                if not self.is_playing:
                    if event.key == pygame.K_SPACE:
                        self.is_playing = True
                        self.reset_game()
                elif self.game_state.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                elif not self.is_paused:  # Only handle movement when not paused
                    self.input_handler.handle_input(event, self.snake, self.food)

    def on_speed_change(self, new_speed):
        self.current_speed = new_speed
    
    def on_pause_toggle(self, is_paused):
        self.is_paused = is_paused
        if not is_paused:
            self.last_update_time = time.time()  # Reset update time when unpausing

    def update(self):
        current_time = time.time()
        update_interval = 1.0 / self.current_speed

        if not self.game_state.game_over and not self.is_paused:
            # Only update if enough time has passed
            if current_time - self.last_update_time >= update_interval:
                # Handle AI input if in AI mode
                if self.input_handler.control_type == "ai":
                    self.input_handler.handle_input(None, self.snake, self.food)
                
                # Update snake position and check for game over
                if not self.snake.move():
                    self.game_state.game_over = True
                else:
                    # Update game state (food collection, etc)
                    self.game_state.update(self.snake, self.food)
                    
                    # Update stats window if it exists
                    if self.stats_window:
                        self.stats_window.update_stats(
                            self.game_state.score,
                            self.snake.get_turns(),
                            len(self.snake.body),
                            GRID_SIZE
                        )
                
                self.last_update_time = current_time

    def run(self):
        while self.is_running:
            self.handle_events()
            
            if not self.is_playing:
                self.renderer.draw_start_screen()
                self.clock.tick(FPS)
                continue
            
            self.update()
            self.renderer.render(
                self.game_state,
                self.snake,
                self.food,
                is_ai_mode=(self.input_handler.control_type == "ai"),
                ai_name=self.input_handler.get_current_ai_name(),
                current_path=self.input_handler.get_current_path()
            )
            
            # Maintain smooth rendering
            pygame.display.flip()
            self.clock.tick(60)  # Cap at 60 FPS for smooth rendering
        
        pygame.quit() 