import pygame
import pygame.gfxdraw
from src.utils.settings import (
    GRID_SIZE, CELL_SIZE, WINDOW_SIZE, CELL_PADDING,
    BACKGROUND, GRID_COLOR, SNAKE_HEAD, SNAKE_BODY_BASE,
    SNAKE_OUTLINE, FOOD_COLOR, FOOD_OUTLINE,
    WHITE, SCORE_COLOR, GAME_OVER_COLOR,
    FOOD_SIZE_FACTOR, TITLE_COLOR, START_TEXT_COLOR,
    PATH_COLOR, SNAKE_COLOR_SCHEMES
)

class Renderer:
    def __init__(self, screen, color_scheme="blue"):
        self.screen = screen
        pygame.font.init()
        self.score_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 100)
        self.game_over_font = pygame.font.Font(None, 74)
        self.info_font = pygame.font.Font(None, 36)
        self.color_scheme = SNAKE_COLOR_SCHEMES[color_scheme]  # Store the selected color scheme
        
        # Path visualization colors
        self.PATH_DOT = (147, 112, 219, 128)  # Semi-transparent purple
        self.PATH_LINE = (255, 255, 0, 64)    # Semi-transparent yellow
    
    def draw_grid(self):
        for i in range(GRID_SIZE):
            pygame.draw.line(
                self.screen, 
                GRID_COLOR,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, WINDOW_SIZE),
                1
            )
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, i * CELL_SIZE),
                (WINDOW_SIZE, i * CELL_SIZE),
                1
            )

    def draw_snake(self, snake):
        if not snake.body:
            return
        
        # Get current color scheme (using self.color_scheme directly)
        head_color = self.color_scheme['head']
        body_color = self.color_scheme['body']
        
        # Create points for the snake's body
        points = []
        for segment in snake.body:
            x = segment[0] * CELL_SIZE + CELL_SIZE // 2
            y = segment[1] * CELL_SIZE + CELL_SIZE // 2
            points.append((x, y))
        
        thickness = CELL_SIZE - (CELL_PADDING * 2)  # Base thickness
        line_thickness = thickness + 1  # Slightly thicker lines to cover circle edges
        outline_thickness = thickness + 4  # Thickness for outline
        
        # First pass: Draw outline circles
        for i, pos in enumerate(points):
            # Draw filled circle and anti-aliased edge for outline
            pygame.gfxdraw.filled_circle(
                self.screen,
                int(pos[0]), int(pos[1]),
                outline_thickness // 2,
                SNAKE_OUTLINE
            )
            pygame.gfxdraw.aacircle(
                self.screen,
                int(pos[0]), int(pos[1]),
                outline_thickness // 2,
                SNAKE_OUTLINE
            )
        
        # Second pass: Draw outline lines
        for i in range(max(0, len(points) - 1)):
            start_pos = points[i]
            end_pos = points[i + 1]
            pygame.draw.line(
                self.screen,
                SNAKE_OUTLINE,
                start_pos,
                end_pos,
                outline_thickness
            )
        
        # Third pass: Draw circles at each joint with anti-aliasing
        for i, pos in enumerate(points):
            # Calculate gradient color from head to body
            darkness = min(i * 1.5, 40)
            r = max(head_color[0] - darkness, body_color[0])
            g = max(head_color[1] - darkness, body_color[1])
            b = max(head_color[2] - darkness, body_color[2])
            color = (r, g, b)
            
            # Use head color for first segment
            if i == 0:
                color = head_color
            
            # Draw filled circle and anti-aliased edge
            pygame.gfxdraw.filled_circle(
                self.screen,
                int(pos[0]), int(pos[1]),
                thickness // 2,
                color
            )
            pygame.gfxdraw.aacircle(
                self.screen,
                int(pos[0]), int(pos[1]),
                thickness // 2,
                color
            )
        
        # Fourth pass: Draw the connecting lines on top
        for i in range(max(0, len(points) - 1)):
            start_pos = points[i]
            end_pos = points[i + 1]
            
            # Calculate gradient color
            darkness = min(i * 1.5, 40)
            r = max(head_color[0] - darkness, body_color[0])
            g = max(head_color[1] - darkness, body_color[1])
            b = max(head_color[2] - darkness, body_color[2])
            color = (r, g, b)
            
            # Draw line segment
            pygame.draw.line(
                self.screen,
                color,
                start_pos,
                end_pos,
                line_thickness
            )
    
    def draw_food(self, food):
        food_size = int(CELL_SIZE * FOOD_SIZE_FACTOR)
        center_x = food.position[0] * CELL_SIZE + CELL_SIZE // 2
        center_y = food.position[1] * CELL_SIZE + CELL_SIZE // 2
        
        # Draw outline with anti-aliasing
        pygame.gfxdraw.filled_circle(
            self.screen,
            center_x, center_y,
            food_size // 2 + 1,
            FOOD_OUTLINE
        )
        pygame.gfxdraw.aacircle(
            self.screen,
            center_x, center_y,
            food_size // 2 + 1,
            FOOD_OUTLINE
        )
        
        # Draw inner circle with anti-aliasing
        pygame.gfxdraw.filled_circle(
            self.screen,
            center_x, center_y,
            food_size // 2,
            FOOD_COLOR
        )
        pygame.gfxdraw.aacircle(
            self.screen,
            center_x, center_y,
            food_size // 2,
            FOOD_COLOR
        )
    
    def draw_path(self, path):
        if not path:
            return
        
        # Create a semi-transparent surface for the path highlight
        path_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        path_surface.set_alpha(64)  # Make it semi-transparent
        # Use a lighter shade of the grid color (GRID_COLOR is 70, 74, 82)
        path_surface.fill((100, 104, 112))  # Lighter gray that matches the grid theme
        
        # Draw highlighted cells for each position in the path
        for pos in path:
            x = pos[0] * CELL_SIZE
            y = pos[1] * CELL_SIZE
            self.screen.blit(path_surface, (x, y))
    
    def draw_score(self, score, is_ai_mode=False, ai_name=None):
        # Draw score
        score_text = self.score_font.render(f'Score: {score}', True, SCORE_COLOR)
        score_rect = score_text.get_rect(topleft=(10, 10))
        self.screen.blit(score_text, score_rect)
        
        # Draw AI mode indicator if active
        if is_ai_mode and ai_name:
            ai_text = self.score_font.render(f'AI: {ai_name}', True, START_TEXT_COLOR)
            ai_rect = ai_text.get_rect(topright=(WINDOW_SIZE - 10, 10))
            self.screen.blit(ai_text, ai_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(128)
        overlay.fill(BACKGROUND)
        self.screen.blit(overlay, (0, 0))

        text = self.game_over_font.render('Game Over', True, GAME_OVER_COLOR)
        text_rect = text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
        
        shadow_text = self.game_over_font.render('Game Over', True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(text, text_rect)

        # Add restart instruction
        restart_text = self.info_font.render('Press SPACE to restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def draw_start_screen(self):
        self.screen.fill(BACKGROUND)
        self.draw_grid()

        # Draw title
        title_text = self.title_font.render('SNAKE', True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/3))
        
        # Add shadow to title
        shadow_text = self.title_font.render('SNAKE', True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)

        # Draw instructions
        instructions = [
            'Controls:',
            'WASD or Arrow Keys to move',
            'TAB to toggle AI mode',
            '1: A* Algorithm',
            '2: Hamiltonian Cycle',
            '3: Greedy Algorithm',
            'Press SPACE to start',
            'Press ESC to quit'
        ]
        
        y_offset = WINDOW_SIZE/2
        for instruction in instructions:
            text = self.info_font.render(instruction, True, START_TEXT_COLOR)
            rect = text.get_rect(center=(WINDOW_SIZE/2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 40

    def render(self, game_state, snake, food, is_ai_mode=False, ai_name=None, current_path=None):
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        
        # Draw the planned path if in AI mode and path exists
        if is_ai_mode and current_path:
            self.draw_path(current_path)
        
        self.draw_food(food)
        self.draw_snake(snake)
        self.draw_score(game_state.score, is_ai_mode, ai_name)
        
        if game_state.game_over:
            self.draw_game_over()
        
        pygame.display.flip()