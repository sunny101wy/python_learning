import pygame
import random

# 初始化 Pygame
pygame.init()

# 游戏窗口尺寸
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# 颜色定义
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
COLORS = [
    (0, 255, 255),   # I
    (255, 255, 0),   # O
    (128, 0, 128),   # T
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (0, 0, 255),     # J
    (255, 165, 0),   # L
]

# 方块形状
SHAPES = [
    [[1, 1, 1, 1]],                          # I
    [[1, 1], [1, 1]],                        # O
    [[0, 1, 0], [1, 1, 1]],                  # T
    [[0, 1, 1], [1, 1, 0]],                  # S
    [[1, 1, 0], [0, 1, 1]],                  # Z
    [[1, 0, 0], [1, 1, 1]],                  # J
    [[0, 0, 1], [1, 1, 1]],                  # L
]

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 方块类
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 判断是否为有效移动
def valid_move(shape, grid, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = x + j
                new_y = y + i
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

# 消除已满的行
def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_grid)
    return [[0] * COLS for _ in range(cleared)] + new_grid, cleared

# 画网格和方块
def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            val = grid[y][x]
            color = val if val else GRAY
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

# 主函数
def main():
    clock = pygame.time.Clock()
    grid = [[0] * COLS for _ in range(ROWS)]
    current = Tetromino()
    fall_time = 0
    game_over = False

    while True:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_move(current.shape, grid, current.x - 1, current.y):
                    current.x -= 1
                elif event.key == pygame.K_RIGHT and valid_move(current.shape, grid, current.x + 1, current.y):
                    current.x += 1
                elif event.key == pygame.K_DOWN and valid_move(current.shape, grid, current.x, current.y + 1):
                    current.y += 1
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*current.shape[::-1])]
                    if valid_move(rotated, grid, current.x, current.y):
                        current.shape = rotated

        if not game_over and fall_time > 500:
            if valid_move(current.shape, grid, current.x, current.y + 1):
                current.y += 1
            else:
                for i, row in enumerate(current.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            new_x = current.x + j
                            new_y = current.y + i
                            if new_y < 0:
                                game_over = True
                            else:
                                grid[new_y][new_x] = current.color
                grid, _ = clear_rows(grid)
                current = Tetromino()
                # ✅ 检查新方块生成位置是否合法
                if not valid_move(current.shape, grid, current.x, current.y):
                    game_over = True
            fall_time = 0

        screen.fill(BLACK)
        draw_grid(grid)

        # 画当前方块
        if not game_over:
            for i, row in enumerate(current.shape):
                for j, cell in enumerate(row):
                    if cell and current.y + i >= 0:
                        pygame.draw.rect(
                            screen,
                            current.color,
                            ((current.x + j) * BLOCK_SIZE, (current.y + i) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                        )

        if game_over:
            font = pygame.font.SysFont(None, 48)
            text = font.render("游戏结束", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

# 启动游戏
if __name__ == "__main__":
    main()
