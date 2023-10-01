from pico2d import *
from collections import deque
import math

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

direction = 0  # 0: left, 1: right
move_speed = 20
target_queue = deque()  # 마우스 클릭 위치를 저장할 큐

def move_towards_target(x, y):
    global direction
    if not target_queue:  # 타겟이 없으면 이동하지 않음
        return x, y

    target_x, target_y = target_queue[0]  # 큐의 첫 번째 타겟으로 이동
    dx, dy = 0, 0
    distance_x = target_x - x
    distance_y = target_y - y
    theta = math.atan2(distance_y, distance_x)
    dx = move_speed * math.cos(theta)
    dy = move_speed * math.sin(theta)

    if dx > 0:
        direction = 1
    else:
        direction = 0

    if math.sqrt((x + dx - target_x) ** 2 + (y + dy - target_y) ** 2) < move_speed:
        x, y = target_x, target_y
        target_queue.popleft()  # 타겟 도착시 큐에서 제거
    else:
        x += dx
        y += dy

    return x, y

def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            target_x, target_y = event.x, TUK_HEIGHT - 1 - event.y
            target_queue.append((target_x, target_y))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass



running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
#hide_cursor()

while running:
    x, y = move_towards_target(x, y)
    
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    for target in target_queue:  # 모든 타겟에 대해 hand_arrow를 그림
        hand_arrow.draw(*target)
    if direction == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    else:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)
    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()




