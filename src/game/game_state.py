from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .snake import Snake
    from .food import Food

class GameState:
    def __init__(self):
        self.score = 0
        self.game_over = False
    
    def update(self, snake: 'Snake', food: 'Food') -> None:
        """Update game state based on snake and food positions"""
        # Check if snake ate food
        if snake.body[0] == food.position:
            self.score += 1
            snake.grow()
            food.spawn(snake.body)
    
    def reset(self) -> None:
        """Reset game state to initial values"""
        self.score = 0
        self.game_over = False