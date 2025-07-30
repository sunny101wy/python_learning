import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("超级马里奥游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
SKY_TOP = (50, 150, 255)  # 天空顶部颜色
SKY_BOTTOM = (150, 200, 255)  # 天空底部颜色
CLOUD_COLOR = (255, 255, 255)  # 云颜色
HILL_COLOR = (0, 100, 0)  # 山丘颜色
SKIN_COLOR = (255, 204, 153)  # 肤色

# 字体设置
font = pygame.font.SysFont("arial", 24)

# 玩家设置
player_width, player_height = 40, 60
player_x, player_y = 50, HEIGHT - player_height - 10
player_speed = 5
player_jump = -15
player_gravity = 0.8
player_vel_y = 0
is_jumping = False
invulnerable = False
invulnerable_timer = 0
INVULNERABLE_DURATION = 120  # 2秒无敌（60帧/秒）
lives = 10
  # 初始生命值
MAX_LIVES = 20 # 生命上限
score = 0  # 初始分数
last_direction = 1  # 1: 右, -1: 左

# 敌人设置
enemy_width, enemy_height = 30, 30
enemy_base_speed = 3
enemy_gravity = 0.8

# 金币设置
coin_width, coin_height = 20, 20
coin_frame_duration = 10  # 每10帧切换动画
coin_frames = []  # 存储金币动画帧
try:
    coin_sprite = pygame.image.load("coin_sprite.png")
    for i in range(4):
        frame = coin_sprite.subsurface((i * coin_width, 0, coin_width, coin_height))
        coin_frames.append(pygame.transform.scale(frame, (coin_width, coin_height)))
    print("金币精灵图加载成功")
except FileNotFoundError:
    print("错误：未找到 coin_sprite.png，将使用黄色矩形替代")
    coin_frames = [None]

# 平台、敌人、金币和背景列表
platforms = [
    pygame.Rect(0, HEIGHT - 10, WIDTH, 10),
    pygame.Rect(200, 400, 200, 20),
]
enemies = []
coins = []
clouds = []
hills = []

# 关卡管理
current_level = 1
max_platforms = 3
max_enemies = 2
max_coins = 3

# 绘制像素马里奥
def draw_pixel_mario(x, y, direction):
    pixel_size = 2  # 每个像素为2x2方块
    # 16x32 像素网格，缩放为 32x64
    for row in range(32):
        for col in range(16):
            # 翻转 x 坐标
            draw_col = col if direction == 1 else 15 - col
            pixel_x = x - 4 + draw_col * pixel_size  # 居中偏移
            pixel_y = y + 2 + row * pixel_size
            color = None
            # 头部（0-8行）
            if 0 <= row < 8:
                if 3 <= col <= 12 and 0 <= row <= 2:  # 帽子
                    color = RED
                elif 4 <= col <= 10 and 3 <= row <= 7:  # 脸
                    color = SKIN_COLOR
                elif col in [6, 7] and row == 4:  # 眼睛（黑色）
                    color = BLACK
                elif col == 6 and row == 4:  # 眼睛高光（白色）
                    color = WHITE
                elif 8 <= col <= 9 and 5 <= row <= 6:  # 鼻子
                    color = SKIN_COLOR
                elif 7 <= col <= 10 and 6 <= row <= 7:  # 胡子
                    color = BLACK
            # 身体（8-24行）
            elif 8 <= row < 24:
                if 4 <= col <= 12 and 8 <= row <= 11:  # 衬衫
                    color = RED
                elif 4 <= col <= 12 and 12 <= row <= 19:  # 背带裤
                    color = BLUE
                elif (2 <= col <= 3 or 12 <= col <= 13) and 10 <= row <= 11:  # 手
                    color = SKIN_COLOR
            # 腿部（24-32行）
            elif 24 <= row < 32:
                if 6 <= col <= 10 and 24 <= row <= 27:  # 裤子
                    color = BLUE
                if 5 <= col <= 11 and 28 <= row <= 31:  # 鞋
                    color = BLACK
            if color:
                pygame.draw.rect(screen, color, (pixel_x, pixel_y, pixel_size, pixel_size))

# 生成新关卡
def generate_level(level):
    global platforms, enemies, coins, clouds, hills
    print(f"生成关卡 {level}...")
    platforms = [pygame.Rect(0, HEIGHT - 10, WIDTH, 10)]
    enemies = []
    coins = []
    clouds = []
    hills = []
    num_platforms = min(random.randint(1, max_platforms + level // 3), 5)
    for _ in range(num_platforms):
        x = random.randint(100, WIDTH - 200)
        y = random.randint(250, 450)
        width = random.randint(100, 250)
        platforms.append(pygame.Rect(x, y, width, 20))
    num_enemies = min(random.randint(1, max_enemies + level // 5), 4)
    for i in range(num_enemies):
        x = random.randint(100, WIDTH - 100)
        y = HEIGHT - enemy_height - 10
        enemy_type = random.choice(["Patrol", "Chaser"])
        speed = enemy_base_speed * random.uniform(0.8, 1.2)
        enemies.append({
            "rect": pygame.Rect(x, y, enemy_width, enemy_height),
            "direction": random.choice([-1, 1]),
            "type": enemy_type,
            "speed": speed,
            "vel_y": 0,
            "id": f"敌人_{level}_{i}"
        })
    num_coins = random.randint(1, max_coins)
    for i in range(num_coins):
        platform = random.choice(platforms)
        x = random.randint(platform.left, platform.right - coin_width)
        y = platform.top - coin_height - 5
        coins.append({
            "rect": pygame.Rect(x, y, coin_width, coin_height),
            "id": f"金币_{level}_{i}",
            "frame": 0,
            "frame_timer": 0
        })
    num_clouds = random.randint(3, 5)
    for _ in range(num_clouds):
        x = random.randint(50, WIDTH - 100)
        y = random.randint(50, HEIGHT // 2)
        width = random.randint(50, 100)
        height = width // 2
        clouds.append({"x": x, "y": y, "width": width, "height": height})
    num_hills = random.randint(2, 3)
    for i in range(num_hills):
        base_x = i * (WIDTH // num_hills) + random.randint(-50, 50)
        base_width = random.randint(150, 250)
        height = random.randint(100, 200)
        points = [
            (base_x, HEIGHT),
            (base_x + base_width, HEIGHT),
            (base_x + base_width // 2, HEIGHT - height)
        ]
        hills.append({"points": points})
    print(f"关卡 {level}: {num_platforms} 个平台, {num_enemies} 个敌人, {num_coins} 个金币, {num_clouds} 个云, {num_hills} 个山丘")

# 淡入淡出过渡
def transition_screen():
    for alpha in range(0, 255, 5):
        screen.fill(BLACK)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        time.sleep(0.01)
    for alpha in range(255, 0, -5):
        screen.fill(BLACK)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        time.sleep(0.01)

# Game Over 屏幕
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("游戏结束！", True, WHITE)
    final_score_text = font.render(f"最终分数: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))
    screen.blit(final_score_text, (WIDTH // 2 - 50, HEIGHT // 2 + 10))
    pygame.display.flip()
    time.sleep(3)

# 绘制程序化背景
def draw_background():
    for y in range(HEIGHT):
        r = SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * y / HEIGHT
        g = SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * y / HEIGHT
        b = SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * y / HEIGHT
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))
    for cloud in clouds:
        pygame.draw.ellipse(screen, CLOUD_COLOR, (cloud["x"], cloud["y"], cloud["width"], cloud["height"]))
    for hill in hills:
        pygame.draw.polygon(screen, HILL_COLOR, hill["points"])

# 检查敌人是否在平台上
def is_on_platform(enemy_rect, platforms):
    check_rect = enemy_rect.copy()
    check_rect.y += 1
    for platform in platforms:
        if check_rect.colliderect(platform):
            return platform
    return None

# 游戏主循环
clock = pygame.time.Clock()
running = True
trigger_zone = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)
game_over = False

generate_level(current_level)

while running:
    if game_over:
        game_over_screen()
        break

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = player_jump
                is_jumping = True

    # 玩家移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        last_direction = -1
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        last_direction = 1

    # 应用重力
    player_vel_y += player_gravity
    player_y += player_vel_y

    # 创建玩家矩形
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # 碰撞检测 - 平台
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_vel_y > 0:
                player_y = platform.top - player_height
                player_vel_y = 0
                is_jumping = False
            elif player_vel_y < 0:
                player_y = platform.bottom
                player_vel_y = 0

    # 无敌计时
    if invulnerable:
        invulnerable_timer -= 1
        if invulnerable_timer <= 0:
            invulnerable = False

    # 敌人行为
    enemies_to_remove = []
    for enemy in enemies:
        if enemy["type"] == "Patrol":
            next_x = enemy["rect"].x + enemy["speed"] * enemy["direction"]
            test_rect = enemy["rect"].copy()
            test_rect.x = next_x
            if is_on_platform(test_rect, platforms) and 0 < next_x < WIDTH - enemy_width:
                enemy["rect"].x = next_x
            else:
                enemy["direction"] *= -1
        elif enemy["type"] == "Chaser":
            if player_rect.centerx > enemy["rect"].centerx:
                enemy["direction"] = 1
            else:
                enemy["direction"] = -1
            next_x = enemy["rect"].x + enemy["speed"] * enemy["direction"]
            if is_on_platform(enemy["rect"], platforms) and 0 < next_x < WIDTH - enemy_width:
                enemy["rect"].x = next_x

        enemy["vel_y"] += enemy_gravity
        enemy["rect"].y += enemy["vel_y"]
        platform = is_on_platform(enemy["rect"], platforms)
        if platform and enemy["vel_y"] > 0:
            enemy["rect"].y = platform.top - enemy_height
            enemy["vel_y"] = 0

        if player_rect.colliderect(enemy["rect"]) and not invulnerable:
            if player_vel_y > 0 and player_rect.bottom < enemy["rect"].centery:
                enemies_to_remove.append(enemy)
                player_vel_y = player_jump * 0.5
                score += 200
                print(f"消灭 {enemy['id']}，+200分，当前分数: {score}")
            else:
                lives -= 1
                print(f"玩家被 {enemy['id']} 击中！剩余生命: {lives}")
                invulnerable = True
                invulnerable_timer = INVULNERABLE_DURATION
                if player_rect.centerx > enemy["rect"].centerx:
                    player_x += 50
                else:
                    player_x -= 50
                player_vel_y = player_jump * 0.5
                if lives <= 0:
                    game_over = True

    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    # 金币动画和收集
    coins_to_remove = []
    coin_list = list(coins)
    for coin in coin_list:
        coin["frame_timer"] += 1
        if coin["frame_timer"] >= coin_frame_duration:
            coin["frame"] = (coin["frame"] + 1) % 4
            coin["frame_timer"] = 0
            print(f"{coin['id']} 切换到帧 {coin['frame']}")
        if player_rect.colliderect(coin["rect"]):
            score += 100
            print(f"收集 {coin['id']}，+100分，当前分数: {score}")
            if lives < MAX_LIVES:
                lives += 1
                print(f"生命恢复！当前生命: {lives}")
            else:
                print(f"生命已满！")
            coins_to_remove.append(coin)

    for coin in coins_to_remove:
        coins.remove(coin)

    # 防止玩家掉出屏幕
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_vel_y = 0
        is_jumping = False

    # 关卡刷新
    if player_rect.colliderect(trigger_zone):
        print(f"玩家进入触发区域 x={player_x}")
        transition_screen()
        player_x = 50
        current_level += 1
        generate_level(current_level)

    # 绘制
    draw_background()
    if not invulnerable or (invulnerable and invulnerable_timer % 4 < 2):
        draw_pixel_mario(player_x, player_y, last_direction)
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])
        arrow_start = enemy["rect"].center
        arrow_end = (arrow_start[0] + 10 * enemy["direction"], arrow_start[1])
        pygame.draw.line(screen, YELLOW, arrow_start, arrow_end, 3)
    for coin in coins:
        if coin_frames[0] is None:
            pygame.draw.rect(screen, YELLOW, coin["rect"])
        else:
            screen.blit(coin_frames[coin["frame"]], coin["rect"])
    pygame.draw.rect(screen, (0, 0, 255, 50), trigger_zone, 2)
    level_text = font.render(f"关卡: {current_level}", True, BLACK)
    lives_text = font.render(f"生命: {lives}", True, BLACK)
    score_text = font.render(f"分数: {score}", True, BLACK)
    screen.blit(level_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(score_text, (10, 70))
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()