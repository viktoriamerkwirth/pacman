import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 560, 620
CELL_SIZE = 20
ROWS, COLS = 31, 28

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Maze layout (1 = wall, 0 = path, 2 = pellet, 3 = power pellet)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class PacMan:
    def __init__(self):
        self.x = 14
        self.y = 23
        self.direction = Direction.LEFT
        self.next_direction = Direction.LEFT
        self.mouth_open = 0
        self.power_mode = 0  # Frames remaining in power mode
        
    def move(self):
        # Try to change direction
        next_x = self.x + self.next_direction.value[0]
        next_y = self.y + self.next_direction.value[1]
        
        if 0 <= next_x < COLS and 0 <= next_y < ROWS and maze[next_y][next_x] != 1:
            self.direction = self.next_direction
        
        # Move in current direction
        new_x = self.x + self.direction.value[0]
        new_y = self.y + self.direction.value[1]
        
        # Wrap around
        if new_x < 0:
            new_x = COLS - 1
        elif new_x >= COLS:
            new_x = 0
            
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
            
        self.mouth_open = (self.mouth_open + 1) % 20
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Draw Pac-Man with animated mouth
        if self.mouth_open < 10:
            angle = 45
        else:
            angle = 0
            
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        
        # Draw mouth
        if angle > 0:
            mouth_angle = angle
            if self.direction == Direction.RIGHT:
                start_angle = -mouth_angle
                end_angle = mouth_angle
            elif self.direction == Direction.LEFT:
                start_angle = 180 - mouth_angle
                end_angle = 180 + mouth_angle
            elif self.direction == Direction.UP:
                start_angle = 270 - mouth_angle
                end_angle = 270 + mouth_angle
            else:  # DOWN
                start_angle = 90 - mouth_angle
                end_angle = 90 + mouth_angle
            
            points = [(center_x, center_y)]
            for angle in range(int(start_angle), int(end_angle) + 1, 5):
                x = center_x + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                y = center_y + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((x, y))
            points.append((center_x, center_y))
            
            if len(points) > 2:
                pygame.draw.polygon(screen, BLACK, points)

class Ghost:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.direction = Direction.LEFT
        self.eaten = False
        
    def move(self, pacman):
        # If eaten, return to start position
        if self.eaten:
            if self.x == self.start_x and self.y == self.start_y:
                self.eaten = False
            else:
                # Move towards start position
                if self.x < self.start_x:
                    self.x += 1
                elif self.x > self.start_x:
                    self.x -= 1
                elif self.y < self.start_y:
                    self.y += 1
                elif self.y > self.start_y:
                    self.y -= 1
                return
        
        # Simple AI: try to move towards Pac-Man (or away if power mode)
        possible_moves = []
        
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            new_x = self.x + direction.value[0]
            new_y = self.y + direction.value[1]
            
            # Wrap around
            if new_x < 0:
                new_x = COLS - 1
            elif new_x >= COLS:
                new_x = 0
            
            if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != 1:
                distance = abs(new_x - pacman.x) + abs(new_y - pacman.y)
                possible_moves.append((distance, new_x, new_y, direction))
        
        if possible_moves:
            # If Pac-Man is in power mode, run away (choose furthest move)
            if pacman.power_mode > 0:
                possible_moves.sort(key=lambda x: x[0], reverse=True)
            else:
                possible_moves.sort(key=lambda x: x[0])
            _, self.x, self.y, self.direction = possible_moves[0]
    
    def draw(self, screen, power_mode):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # If eaten, draw eyes only
        if self.eaten:
            pygame.draw.circle(screen, WHITE, (center_x - 3, center_y), 4)
            pygame.draw.circle(screen, WHITE, (center_x + 3, center_y), 4)
            pygame.draw.circle(screen, BLUE, (center_x - 3, center_y), 2)
            pygame.draw.circle(screen, BLUE, (center_x + 3, center_y), 2)
            return
        
        # Color changes when vulnerable
        ghost_color = (0, 0, 150) if power_mode > 0 else self.color
        
        # Body
        pygame.draw.circle(screen, ghost_color, (center_x, center_y - 2), radius)
        pygame.draw.rect(screen, ghost_color, (center_x - radius, center_y - 2, radius * 2, radius))
        
        # Wavy bottom
        wave_width = radius * 2 // 3
        for i in range(3):
            x = center_x - radius + i * wave_width
            pygame.draw.circle(screen, ghost_color, (x + wave_width // 2, center_y + radius - 2), wave_width // 2)
        
        # Eyes
        eye_offset = radius // 3
        pygame.draw.circle(screen, WHITE, (center_x - eye_offset, center_y - 3), 4)
        pygame.draw.circle(screen, WHITE, (center_x + eye_offset, center_y - 3), 4)
        pygame.draw.circle(screen, BLUE, (center_x - eye_offset, center_y - 3), 2)
        pygame.draw.circle(screen, BLUE, (center_x + eye_offset, center_y - 3), 2)

def draw_maze(screen):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 2)
            elif maze[row][col] == 3:
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 5)

def reset_maze():
    """Reset the maze to its original state with all pellets"""
    global maze
    maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
        [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
        [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
        [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
        [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
        [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
        [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
        [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
        [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
        [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
        [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
        [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
        [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
        [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
        [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

def count_pellets():
    """Count remaining pellets in the maze"""
    count = 0
    for row in maze:
        for cell in row:
            if cell == 2 or cell == 3:
                count += 1
    return count

def create_power_sound():
    """Create a spooky sound effect for power mode"""
    duration = 0.3
    sample_rate = 22050
    # Create descending tone for spooky effect
    t = pygame.sndarray.make_sound(
        (32767 * 0.3 * (
            0.5 * (1 + pygame.math.Vector2(1, 0).rotate(
                360 * 220 * t / sample_rate - 100 * t * t / (sample_rate * sample_rate)
            ).x)
        )).astype('int16')
        for t in range(int(duration * sample_rate))
    )
    return t

def create_eat_ghost_sound():
    """Create a sound effect for eating ghosts"""
    duration = 0.2
    sample_rate = 22050
    import numpy as np
    # Create ascending tone
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t * (1 + t * 2))
    wave = (wave * 32767 * 0.3).astype('int16')
    sound = pygame.sndarray.make_sound(wave)
    return sound

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    
    # Create sound effects
    try:
        import numpy as np
        power_sound = create_power_sound()
        eat_ghost_sound = create_eat_ghost_sound()
    except:
        power_sound = None
        eat_ghost_sound = None
    
    pacman = PacMan()
    ghosts = [
        Ghost(13, 14, RED),
        Ghost(14, 14, PINK),
        Ghost(13, 15, CYAN),
        Ghost(14, 15, ORANGE)
    ]
    
    score = 0
    level = 1
    font = pygame.font.Font(None, 36)
    
    move_counter = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pacman.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pacman.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pacman.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pacman.next_direction = Direction.RIGHT
        
        # Move Pac-Man
        pacman.move()
        
        # Update power mode timer
        if pacman.power_mode > 0:
            pacman.power_mode -= 1
        
        # Check pellet collection
        if maze[pacman.y][pacman.x] == 2:
            maze[pacman.y][pacman.x] = 0
            score += 10
        elif maze[pacman.y][pacman.x] == 3:
            maze[pacman.y][pacman.x] = 0
            score += 50
            pacman.power_mode = 100  # Power mode lasts 100 frames (10 seconds)
            if power_sound:
                power_sound.play()
        
        # Check if all pellets are collected
        if count_pellets() == 0:
            level += 1
            reset_maze()
            pacman.x = 14
            pacman.y = 23
            for ghost in ghosts:
                ghost.x = ghost.start_x
                ghost.y = ghost.start_y
        
        # Move ghosts (slower than Pac-Man)
        move_counter += 1
        if move_counter % 2 == 0:
            for ghost in ghosts:
                ghost.move(pacman)
        
        # Check collision with ghosts
        for ghost in ghosts:
            if pacman.x == ghost.x and pacman.y == ghost.y and not ghost.eaten:
                if pacman.power_mode > 0:
                    # Eat the ghost
                    ghost.eaten = True
                    score += 200
                    if eat_ghost_sound:
                        eat_ghost_sound.play()
                else:
                    # Game over - reset positions
                    pacman.x = 14
                    pacman.y = 23
                    pacman.power_mode = 0
                    for g in ghosts:
                        g.x = g.start_x
                        g.y = g.start_y
                        g.eaten = False
        
        # Draw everything
        screen.fill(BLACK)
        draw_maze(screen)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen, pacman.power_mode)
        
        # Draw score and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        screen.blit(level_text, (WIDTH - 150, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
