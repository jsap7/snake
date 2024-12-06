import pygame
import time
import logging
import traceback
from src.utils.settings import WINDOW_SIZE, FPS, GRID_SIZE
from src.game.snake import Snake
from src.game.food import Food
from src.utils.input_handler import InputHandler
from src.ui.renderer import Renderer
from src.game.game_state import GameState
from src.ui.game_stats import GameStats
from src.ai import AI_ALGORITHMS
import os
import random

class Game:
    def __init__(self, start_with_ai=False, ai_algorithm="astar", speed=10, headless=False, genetic_individual=None, max_steps_multiplier=1):
        # Set SDL to use dummy video driver for headless mode
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        
        # Initialize pygame (needed for timing even in headless mode)
        pygame.init()
        
        self.headless = headless
        self.moves = 0  # Track number of moves for genetic fitness
        self.max_steps_multiplier = max_steps_multiplier
        
        if not self.headless:
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Snake Game")
            self.clock = pygame.time.Clock()
            self.renderer = Renderer(self.screen)
        else:
            # Create a dummy surface for headless mode
            self.screen = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            self.clock = pygame.time.Clock()
        
        # Initialize components
        self.snake = Snake()
        self.food = Food()
        self.input_handler = InputHandler()
        self.game_state = GameState()
        
        # Game flow control
        self.is_running = True
        self.is_playing = True
        self.current_speed = speed
        self.is_paused = False
        self.last_update_time = time.time()
        
        # Set initial control mode and AI algorithm
        if start_with_ai:
            if genetic_individual:
                self.input_handler.set_genetic_individual(genetic_individual)
            self.input_handler.current_ai_name = ai_algorithm
            self.input_handler.set_control_type("ai")
            
            if not self.headless:
                # Create stats window for AI mode with callbacks
                self.stats_window = GameStats(
                    self.input_handler.get_current_ai_name(),
                    speed_callback=self.on_speed_change,
                    pause_callback=self.on_pause_toggle
                )
        else:
            self.input_handler.set_control_type("human")
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

    def run_headless(self):
        """Run the game without rendering for simulation purposes"""
        # Ensure AI is initialized
        if not self.input_handler.current_ai and self.input_handler.current_ai_name:
            ai_class = AI_ALGORITHMS[self.input_handler.current_ai_name]
            self.input_handler.current_ai = ai_class()
            
        if self.headless:
            return self.run_fast_simulation()
        else:
            # For single AI games, use normal rendering
            return self.run()

    def run_fast_simulation(self):
        """Ultra-fast simulation without pygame or rendering"""
        score = 0
        snake_body = [(GRID_SIZE // 2, GRID_SIZE // 2)]  # Start in middle
        food_pos = (GRID_SIZE - 5, GRID_SIZE - 5)  # Initial food position
        growing = False
        
        try:
            while True:  # Run until snake dies or can't continue
                # Get AI's next move using the current_ai instance
                if not self.input_handler.current_ai:
                    raise Exception("No AI algorithm initialized")
                    
                dx, dy = self.input_handler.current_ai.get_next_move(
                    snake_body[0],  # snake head
                    food_pos,       # food position
                    snake_body      # full snake body
                )
                
                # Calculate new head position
                new_head = (snake_body[0][0] + dx, snake_body[0][1] + dy)
                
                # Check wall collision
                if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
                    break
                
                # Check self collision (excluding tail if not growing)
                if new_head in snake_body[:-1] or (new_head in snake_body and not growing):
                    break
                
                # Move snake
                snake_body.insert(0, new_head)
                if not growing:
                    snake_body.pop()
                growing = False
                
                # Check food collision
                if new_head == food_pos:
                    score += 1
                    growing = True
                    
                    # Generate new food position
                    available_positions = [
                        (x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)
                        if (x, y) not in snake_body
                    ]
                    if available_positions:
                        # Try to place food away from snake head
                        distant_positions = [
                            pos for pos in available_positions
                            if abs(pos[0] - new_head[0]) + abs(pos[1] - new_head[1]) > 3
                        ]
                        food_pos = random.choice(distant_positions if distant_positions else available_positions)
                    else:
                        break  # No space left for food
            
            return score
            
        except Exception as e:
            logging.error(f"Error in fast simulation: {str(e)}")
            logging.error(traceback.format_exc())
            return score

    def run_normal_headless(self):
        """Original headless mode with pygame (slower but more accurate)"""
        logging.debug("Starting headless game run")
        
        # Calculate max steps based on grid size and multiplier
        base_max_steps = GRID_SIZE * GRID_SIZE * 4  # Base max steps is 4 times the grid area
        max_steps = base_max_steps * self.max_steps_multiplier
        steps = 0
        steps_without_food = 0  # Track steps without eating food
        max_steps_without_food = GRID_SIZE * 3  # Maximum steps allowed without eating
        
        try:
            while not self.game_state.game_over and steps < max_steps:
                # Handle AI input
                self.input_handler.handle_input(None, self.snake, self.food)
                
                # Update game state
                if not self.snake.move():
                    logging.debug(f"Game over: Snake collision at step {steps}")
                    self.game_state.game_over = True
                else:
                    old_score = self.game_state.score
                    self.game_state.update(self.snake, self.food)
                    
                    # Check if food was eaten
                    if self.game_state.score > old_score:
                        steps_without_food = 0
                        # Spawn food away from current position
                        self.food.spawn(self.snake.body)
                    else:
                        steps_without_food += 1
                        
                        # End game if snake hasn't eaten for too long
                        if steps_without_food >= max_steps_without_food:
                            logging.debug(f"Game over: No food eaten for {steps_without_food} steps")
                            self.game_state.game_over = True
                
                steps += 1
                self.moves = steps
                
                # Maintain consistent game speed
                self.clock.tick(self.current_speed)
                
                if steps >= max_steps:
                    logging.debug("Game reached maximum steps")
            
            logging.debug(f"Headless game completed. Score: {self.game_state.score}, Steps: {steps}")
            return self.game_state.score
            
        except Exception as e:
            logging.error(f"Error in headless game: {str(e)}")
            logging.error(traceback.format_exc())
            raise