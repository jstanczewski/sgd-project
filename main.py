import pygame
import random
import sys
import math

# --- Constants ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 60
GROUND_HEIGHT = 550

# Colors
COLOR_DAY = (235, 235, 235)
COLOR_NIGHT = (50, 50, 50)
COLOR_GROUND = (83, 83, 83)
COLOR_DINO = (0, 0, 0)
COLOR_HIGHLIGHT = (255, 0, 0)
COLOR_INPUT = (0, 0, 0)
COLOR_BG_OVERLAY = (200, 200, 200)

# Dino settings
DINO_WIDTH = 60
DINO_HEIGHT = 60
DINO_X = 100
GRAVITY = 1.0
JUMP_VELOCITY = -20

# Obstacle settings
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 60
PTERO_WIDTH = 70
PTERO_HEIGHT = 60

# Default obstacle speed and spawn interval
OBSTACLE_SPEED = 6
SPAWN_INTERVAL = 1500


def show_main_menu(screen, fonts, background):
    title_font, menu_font = fonts
    options = ['Start Game', 'Instructions', 'Choose Difficulty', 'Choose Character', 'Quit']
    selected = 0
    while True:
        screen.blit(background, (0, 0))
        title = title_font.render('Dino Game', True, COLOR_DINO)
        screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 100))
        for i, text in enumerate(options):
            prefix = '> ' if i == selected else '  '
            surf = menu_font.render(f"{prefix}{text}", True, COLOR_DINO)
            screen.blit(surf, ((WINDOW_WIDTH - surf.get_width()) // 2, 250 + i * 60))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    return options[selected]


def show_instructions(screen, fonts, background):
    title_font, menu_font = fonts
    instructions = [
        'Use SPACE or UP to jump.',
        'Avoid cactuses and pterodactyls.',
        'Press P to pause.',
        'Press ESC to return.'
    ]
    while True:
        screen.blit(background, (0, 0))
        title = title_font.render('Instructions', True, COLOR_DINO)
        screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 100))
        for i, line in enumerate(instructions):
            surf = menu_font.render(line, True, COLOR_DINO)
            screen.blit(surf, ((WINDOW_WIDTH - surf.get_width()) // 2, 200 + i * 50))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return


def show_difficulty_menu(screen, fonts, background):
    title_font, menu_font = fonts
    options = ['Easy', 'Medium', 'Hard', 'Impossible', 'Back']
    speeds = [4, 6, 8, 12]
    intervals = [2000, 1500, 1200, 800]
    selected = 0
    while True:
        screen.blit(background, (0, 0))
        title = title_font.render('Select Difficulty', True, COLOR_DINO)
        screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 100))
        for i, text in enumerate(options):
            prefix = '> ' if i == selected else '  '
            surf = menu_font.render(f"{prefix}{text}", True, COLOR_DINO)
            screen.blit(surf, ((WINDOW_WIDTH - surf.get_width()) // 2, 250 + i * 60))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if options[selected] == 'Back':
                        return None, None, None
                    return options[selected], speeds[selected], intervals[selected]
                elif e.key == pygame.K_ESCAPE:
                    return None, None, None


def show_character_menu(screen, fonts, background, characters):
    thumb = 80;
    pad = 20;
    cols = 4
    keys = list(characters.keys());
    total = len(keys);
    selected = 0
    thumbs = {k: pygame.transform.scale(characters[k], (thumb, thumb)) for k in keys}
    while True:
        screen.blit(background, (0, 0))
        title = fonts[0].render('Select Character', True, COLOR_DINO)
        screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 50))
        start_x = (WINDOW_WIDTH - (thumb * cols + pad * (cols - 1))) // 2
        for idx, key in enumerate(keys):
            row, col = divmod(idx, cols)
            x = start_x + col * (thumb + pad)
            y = 150 + row * (thumb + pad)
            rect = pygame.Rect(x, y, thumb, thumb)
            screen.blit(thumbs[key], rect)
            if idx == selected:
                pygame.draw.rect(screen, COLOR_HIGHLIGHT, rect, 4)
        back = fonts[1].render('Press ESC to go back', True, COLOR_DINO)
        screen.blit(back, ((WINDOW_WIDTH - back.get_width()) // 2, WINDOW_HEIGHT - 50))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    selected = (selected + 1) % total
                elif e.key == pygame.K_LEFT:
                    selected = (selected - 1) % total
                elif e.key == pygame.K_DOWN:
                    selected = (selected + cols) % total
                elif e.key == pygame.K_UP:
                    selected = (selected - cols) % total
                elif e.key == pygame.K_RETURN:
                    return keys[selected]
                elif e.key == pygame.K_ESCAPE:
                    return None


def show_math_minigame(screen, font_large, font_small, background, level):
    # puzzle range depends on current level
    a = random.randint(level, level + 3)
    b = random.randint(level, level + 3)
    answer = a * b
    prompt = f"{a} x {b} = ?"
    user_input = ''
    start_time = pygame.time.get_ticks()
    timeout = 5000
    while True:
        now = pygame.time.get_ticks()
        if now - start_time > timeout:
            return False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif e.key == pygame.K_RETURN:
                    try:
                        return int(user_input) == answer
                    except:
                        return False
                elif e.unicode.isdigit():
                    user_input += e.unicode
        screen.blit(background, (0, 0))
        pygame.draw.line(screen, COLOR_GROUND, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 4)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(COLOR_BG_OVERLAY)
        screen.blit(overlay, (0, 0))
        prompt_surf = font_large.render(prompt, True, COLOR_DINO)
        input_surf = font_large.render(user_input, True, COLOR_INPUT)
        timer = max(0, timeout - (now - start_time)) // 1000 + 1
        timer_surf = font_small.render(f"Time: {timer}", True, COLOR_DINO)
        screen.blit(prompt_surf, ((WINDOW_WIDTH - prompt_surf.get_width()) // 2, WINDOW_HEIGHT // 3))
        screen.blit(input_surf, ((WINDOW_WIDTH - input_surf.get_width()) // 2, WINDOW_HEIGHT // 2))
        screen.blit(timer_surf, (WINDOW_WIDTH - 150, 20))
        pygame.display.flip()
        pygame.time.delay(30)


class Dino:
    def __init__(self):
        self.rect = pygame.Rect(DINO_X, GROUND_HEIGHT - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT)
        self.image = dino_img
        self.velocity = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity = JUMP_VELOCITY
            self.is_jumping = True

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.y >= GROUND_HEIGHT - DINO_HEIGHT:
            self.rect.y = GROUND_HEIGHT - DINO_HEIGHT
            self.is_jumping = False
            self.velocity = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, kind, speed):
        self.kind, self.speed = kind, speed
        if kind == 'cactus':
            self.rect = pygame.Rect(WINDOW_WIDTH, GROUND_HEIGHT - CACTUS_HEIGHT, CACTUS_WIDTH, CACTUS_HEIGHT)
            self.image = cactus_img
        else:
            y = GROUND_HEIGHT - DINO_HEIGHT - PTERO_HEIGHT - random.randint(20, 120)
            self.rect = pygame.Rect(WINDOW_WIDTH, y, PTERO_WIDTH, PTERO_HEIGHT)
            self.image = ptero_img

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def game_loop(screen, clock, font_small, font_pause, difficulty, base_speed, base_interval, background):
    font_large = pygame.font.SysFont(None, 72)
    dino = Dino()
    obstacles = []
    spawn = pygame.time.get_ticks()
    score, level = 0, 1
    speed, interval = base_speed, base_interval
    paused = False

    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_UP) and not paused:
                    dino.jump()
                if e.key == pygame.K_p:
                    paused = not paused
        if paused:
            screen.blit(background, (0, 0))
            pygame.draw.line(screen, COLOR_GROUND, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 4)
            dino.draw(screen)
            for o in obstacles:
                o.draw(screen)
            pause_surf = font_pause.render('Paused - Press P', True, COLOR_DINO)
            screen.blit(pause_surf, ((WINDOW_WIDTH - pause_surf.get_width()) // 2,
                                     (WINDOW_HEIGHT - pause_surf.get_height()) // 2))
            pygame.display.flip()
            continue
        if now - spawn > interval:
            obstacles.append(Obstacle(random.choice(['cactus', 'cactus', 'ptero']), speed))
            spawn = now
        dino.update()
        for o in obstacles[:]:
            o.update()
            if o.rect.right < 0:
                obstacles.remove(o)
                score += 1
                new_lvl = score // 10 + 1
                if new_lvl > level:
                    level = new_lvl
                    speed = base_speed + (level - 1)
        if any(dino.rect.colliderect(o.rect) for o in obstacles):
            # puzzle uses current level for range
            if show_math_minigame(screen, font_large, font_small, background, level):
                obstacles.clear()
                dino.rect.y = GROUND_HEIGHT - DINO_HEIGHT
                spawn = pygame.time.get_ticks()
                continue
            # final death: pulsate
            for i in range(60):
                alpha = abs(math.sin(i / 10 * math.pi)) * 200
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                thickness = 10
                pygame.draw.rect(overlay, (255, 0, 0, int(alpha)), (0, 0, WINDOW_WIDTH, thickness))
                pygame.draw.rect(overlay, (255, 0, 0, int(alpha)), (0, 0, thickness, WINDOW_HEIGHT))
                pygame.draw.rect(overlay, (255, 0, 0, int(alpha)),
                                 (0, WINDOW_HEIGHT - thickness, WINDOW_WIDTH, thickness))
                pygame.draw.rect(overlay, (255, 0, 0, int(alpha)),
                                 (WINDOW_WIDTH - thickness, 0, thickness, WINDOW_HEIGHT))
                screen.blit(background, (0, 0))
                pygame.draw.line(screen, COLOR_GROUND, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 4)
                dino.draw(screen)
                for o in obstacles:
                    o.draw(screen)
                screen.blit(overlay, (0, 0))
                pygame.display.flip()
                clock.tick(FPS)
            return score
        screen.blit(background, (0, 0))
        pygame.draw.line(screen, COLOR_GROUND, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 4)
        dino.draw(screen)
        for o in obstacles:
            o.draw(screen)
        screen.blit(font_small.render(f'Score: {score}', True, COLOR_DINO), (WINDOW_WIDTH - 300, 20))
        screen.blit(font_small.render(f'Difficulty: {difficulty}', True, COLOR_DINO), (WINDOW_WIDTH - 300, 60))
        screen.blit(font_small.render(f'Level: {level}', True, COLOR_DINO), (WINDOW_WIDTH - 300, 100))
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Dino Game')
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 64)
    menu_font = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    font_pause = pygame.font.SysFont(None, 54)

    global dino_img, cactus_img, ptero_img
    character_files = ['dino_1.png', 'dino_2.png', 'dino_3.png', 'dino_4.png']
    characters = {}
    for fn in character_files:
        img = pygame.image.load(f'assets/{fn}').convert_alpha()
        characters[fn] = pygame.transform.scale(img, (DINO_WIDTH, DINO_HEIGHT))
    cactus_img = pygame.image.load('assets/cactus.png').convert_alpha()
    cactus_img = pygame.transform.scale(cactus_img, (CACTUS_WIDTH, CACTUS_HEIGHT))
    ptero_img = pygame.image.load('assets/ptero.png').convert_alpha()
    ptero_img = pygame.transform.scale(ptero_img, (PTERO_WIDTH, PTERO_HEIGHT))
    background = pygame.image.load('assets/background.png').convert()
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    current_char = character_files[0]
    dino_img = characters[current_char]
    current_difficulty = 'Medium'
    base_speed, base_interval = OBSTACLE_SPEED, SPAWN_INTERVAL

    while True:
        choice = show_main_menu(screen, (title_font, menu_font), background)
        if choice == 'Quit':
            pygame.quit();
            sys.exit()
        elif choice == 'Start Game':
            score = game_loop(screen, clock, font_small, font_pause, current_difficulty, base_speed, base_interval,
                              background)
            while True:
                screen.blit(background, (0, 0))
                over_surf = title_font.render('Game Over!', True, COLOR_DINO)
                info_surf = menu_font.render(f'Score: {score}', True, COLOR_DINO)
                prompt_surf = menu_font.render('Press R to Restart or Q to Quit', True, COLOR_DINO)
                screen.blit(over_surf, ((WINDOW_WIDTH - over_surf.get_width()) // 2, 150))
                screen.blit(info_surf, ((WINDOW_WIDTH - info_surf.get_width()) // 2, 250))
                screen.blit(prompt_surf, ((WINDOW_WIDTH - prompt_surf.get_width()) // 2, 350))
                pygame.display.flip()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_r:
                            break
                        elif e.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                else:
                    continue
                break
        elif choice == 'Instructions':
            show_instructions(screen, (title_font, menu_font), background)
        elif choice == 'Choose Difficulty':
            diff, spd, inter = show_difficulty_menu(screen, (title_font, menu_font), background)
            if diff is not None:
                current_difficulty, base_speed, base_interval = diff, spd, inter
        elif choice == 'Choose Character':
            sel = show_character_menu(screen, (title_font, menu_font), background, characters)
            if sel is not None:
                current_char, dino_img = sel, characters[sel]


if __name__ == '__main__':
    main()
