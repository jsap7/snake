import pygame
from typing import Optional, List, Tuple, TYPE_CHECKING
from src.ai import AI_ALGORITHMS

if TYPE_CHECKING:
    from src.game.snake import Snake
    from src.game.food import Food
    from src.ai.base import BaseAI

class InputHandler:
    def __init__(self):
        self.control_type = "human"  # "human" or "ai"
        self.current_ai: Optional['BaseAI'] = None
        self.current_ai_name: Optional[str] = None
        self.current_path: List[Tuple[int, int]] = []
    
    def set_control_type(self, control_type: str) -> None:
        """Set the control type and initialize AI if needed"""
        self.control_type = control_type
        if control_type == "ai" and self.current_ai_name:
            # Initialize the AI algorithm
            ai_class = AI_ALGORITHMS[self.current_ai_name]
            self.current_ai = ai_class()
            self.current_path = []
    
    def handle_input(self, event: Optional[pygame.event.Event], snake: 'Snake', food: 'Food') -> None:
        """Handle input from either human player or AI"""
        if self.control_type == "human":
            if event and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.set_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.set_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction("RIGHT")
        elif self.control_type == "ai" and self.current_ai:
            # Get the next move from AI with proper parameters
            direction = self.current_ai.get_next_move(
                snake.body[0],  # snake head
                food.position,  # food position
                snake.body     # full snake body
            )
            
            # Update current path if AI provides it
            if hasattr(self.current_ai, 'current_path'):
                self.current_path = self.current_ai.current_path
            
            # Convert direction vector to direction string
            if direction == (0, -1):
                snake.set_direction("UP")
            elif direction == (0, 1):
                snake.set_direction("DOWN")
            elif direction == (-1, 0):
                snake.set_direction("LEFT")
            elif direction == (1, 0):
                snake.set_direction("RIGHT")
    
    def get_current_ai_name(self) -> Optional[str]:
        """Get the name of the current AI algorithm"""
        return self.current_ai_name
    
    def get_current_path(self) -> List[Tuple[int, int]]:
        """Return the current planned path of the AI"""
        return self.current_path if self.control_type == "ai" else []