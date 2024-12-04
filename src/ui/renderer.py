import pygame
from src.utils.settings import (
    GRID_SIZE, CELL_SIZE, WINDOW_SIZE, CELL_PADDING,
    BACKGROUND, GRID_COLOR, SNAKE_HEAD, SNAKE_BODY,
    SNAKE_OUTLINE, FOOD_COLOR, FOOD_OUTLINE,
    WHITE, SCORE_COLOR, GAME_OVER_COLOR,
    FOOD_SIZE_FACTOR, TITLE_COLOR, START_TEXT_COLOR
)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.score_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 100)
        self.game_over_font = pygame.font.Font(None, 74)
        self.info_font = pygame.font.Font(None, 36)
        
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

    def draw_snake_segment(self, rect, color, outline_color, radius=8):
        """Helper function to draw a snake segment with outline"""
        pygame.draw.rect(self.screen, outline_color, rect.inflate(4, 4), border_radius=radius)
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)
    
    def draw_snake(self, snake):
        for i, segment in enumerate(snake.body):
            # Get previous and next segments for connection logic
            prev_pos = snake.body[i+1] if i < len(snake.body)-1 else None
            next_pos = snake.body[i-1] if i > 0 else None
            
            base_rect = pygame.Rect(
                segment[0] * CELL_SIZE + CELL_PADDING,
                segment[1] * CELL_SIZE + CELL_PADDING,
                CELL_SIZE - 2 * CELL_PADDING,
                CELL_SIZE - 2 * CELL_PADDING
            )

            # Draw connection to next segment if it exists
            if next_pos:
                connection_rect = base_rect.copy()
                if next_pos[0] > segment[0]:  # Moving right
                    connection_rect.width += CELL_PADDING * 2
                elif next_pos[0] < segment[0]:  # Moving left
                    connection_rect.x -= CELL_PADDING * 2
                    connection_rect.width += CELL_PADDING * 2
                elif next_pos[1] > segment[1]:  # Moving down
                    connection_rect.height += CELL_PADDING * 2
                elif next_pos[1] < segment[1]:  # Moving up
                    connection_rect.y -= CELL_PADDING * 2
                    connection_rect.height += CELL_PADDING * 2
                
                self.draw_snake_segment(connection_rect, 
                                     SNAKE_HEAD if i == 0 else SNAKE_BODY,
                                     SNAKE_OUTLINE,
                                     radius=10 if i == 0 else 6)

            # Draw the main segment
            if i == 0:  # Head
                self.draw_snake_segment(base_rect, SNAKE_HEAD, SNAKE_OUTLINE, radius=12)
            else:  # Body
                self.draw_snake_segment(base_rect, SNAKE_BODY, SNAKE_OUTLINE, radius=8)
    
    def draw_food(self, food):
        food_size = int(CELL_SIZE * FOOD_SIZE_FACTOR)
        center_x = food.position[0] * CELL_SIZE + CELL_SIZE // 2
        center_y = food.position[1] * CELL_SIZE + CELL_SIZE // 2
        
        pygame.draw.circle(self.screen, FOOD_OUTLINE, 
                         (center_x, center_y), food_size // 2 + 1)
        pygame.draw.circle(self.screen, FOOD_COLOR, 
                         (center_x, center_y), food_size // 2)
    
    def draw_path(self, path):
        if not path:
            return
        
        # Create a surface for semi-transparent path visualization
        path_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        
        # Draw path lines first (so they appear under the dots)
        for i in range(len(path) - 1):
            start_pos = (
                path[i][0] * CELL_SIZE + CELL_SIZE // 2,
                path[i][1] * CELL_SIZE + CELL_SIZE // 2
            )
            end_pos = (
                path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2,
                path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2
            )
            pygame.draw.line(path_surface, self.PATH_LINE, start_pos, end_pos, 3)
        
        # Draw path dots
        for pos in path:
            center = (
                pos[0] * CELL_SIZE + CELL_SIZE // 2,
                pos[1] * CELL_SIZE + CELL_SIZE // 2
            )
            pygame.draw.circle(path_surface, self.PATH_DOT, center, CELL_SIZE // 4)
        
        # Blit the path surface onto the main screen
        self.screen.blit(path_surface, (0, 0))
    
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