import pygame  # 파이썬에서 2D 게임 개발할 때 가장 많이 쓰는 라이브러리

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bomberman Game")
        self.clock = pygame.time.Clock()
        self.player = Player(50, 50, 5)  # 플레이어 초기 위치와 속도 설정
        self.running = True

        self.frame = Board(16, 12)  # 보드 생성

    def frame_setup(self):  
        for x in range(16):
            for y in range(12):
                if (x == 0 or x == 15) or (y == 0 or y == 11):    
                    element = Wall(destructible=0)
                    self.frame.place_element(element, x, y)

    def start(self):
        self.frame_setup()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_key_input()  # 키 입력 처리 메서드 호출
            self.update()
            pygame.display.flip()
            self.clock.tick(60)  # FPS 설정

    def handle_key_input(self):
        """키 입력을 처리하는 메서드"""
        keys = pygame.key.get_pressed()

        # 플레이어 이동 처리
        if keys[pygame.K_LEFT]:
            self.player.move('left', self.frame)   # 벽 충돌 감지 추가
        if keys[pygame.K_RIGHT]:
            self.player.move('right', self.frame)  
        if keys[pygame.K_UP]:
            self.player.move('up', self.frame)     
        if keys[pygame.K_DOWN]:
            self.player.move('down', self.frame)   

        # 스페이스바로 폭탄 설치
        if keys[pygame.K_SPACE]:
            self.player.place_bomb()

    def update(self):
        """게임 상태를 업데이트하고 화면에 그립니다."""
        self.screen.fill((0, 0, 0))  # 화면 초기화 (검정색 배경)
        self.screen.blit(self.player.image, (self.player.x, self.player.y)) 
                                     # 플레이어 그리기

        for y in range(self.frame.height):
            for x in range(self.frame.width):
                element = self.frame.grid[y][x]
                if element is not None:
                    self.screen.blit(element.image, (x * 50, y * 50))

    def check_win_condition(self):
        pass

    def quit(self):
        pygame.quit()

class Player:
    def __init__(self, x, y, speed):
        self.x = x  # 플레이어의 x 좌표
        self.y = y  # 플레이어의 y 좌표
        self.lives = 3  # 플레이어의 생명
        self.speed = speed  # 플레이어의 이동 속도
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # 생성한 Surface(플레이어)를 파란색으로 채움
        self.bombs = []  # 플레이어가 설치한 폭탄을 관리
        self.bombs_count = 1  # 플레이어가 설치할 수 있는 폭탄 개수

    def get_rect(self):
        """플레이어의 위치와 크기를 기준으로 Rect 객체를 반환"""
        return pygame.Rect(self.x, self.y, 50, 50)

    def move(self, direction, board):
        original_x = self.x
        original_y = self.y

        match direction:
            case 'left':
                self.x -= self.speed
            case 'right':
                self.x += self.speed
            case 'up':
                self.y -= self.speed
            case 'down':
                self.y += self.speed

        # 충돌 감지
        if self.check_collision(board):
            self.x = original_x  # 충돌이 발생하면 원래 위치로 되돌리기
            self.y = original_y

    def check_collision(self, board):
        """벽과의 충돌을 체크"""
        player_rect = self.get_rect()

        for y in range(board.height):
            for x in range(board.width):
                element = board.grid[y][x]
                if element is not None:
                    wall_rect = pygame.Rect(x * 50, y * 50, 50, 50)  # 벽의 Rect
                    if player_rect.colliderect(wall_rect):
                        return True  # 충돌 발생

        return False  # 충돌 없음

    def place_bomb(self):
        if len(self.bombs) < self.bombs_count:  # 설치할 수 있는 폭탄 개수 제한
            bomb = Bomb(self.x, self.y, timer=3)
            self.bombs.append(bomb)
            print(f"Bomb placed at ({self.x}, {self.y})")  # 콘솔에 폭탄 설치 위치 출력

    def die(self):
        # 사망 처리
        pass

class Bomb:
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer  # 폭탄 타이머 (초)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # 빨간색 폭탄

    def update(self):
        # 폭탄 타이머 업데이트
        pass

    def explode(self):
        # 폭발 처리
        pass

class Wall:
    def __init__(self, destructible):
        self.destructible = destructible
        self.image = pygame.Surface((50, 50))
        self.image.fill((128, 128, 128))

class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def apply_effect(self, player):
        # 아이템 효과 적용
        pass

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def place_element(self, element, x, y):
        self.grid[y][x] = element
        # 보드에 요소 배치
        pass

    def remove_element(self, x, y):
        # 보드에서 요소 제거
        pass

class Explosion:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def affect_elements(self):
        # 폭발 효과 처리
        pass

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        # 적 이동 처리
        pass

    def die(self):
        # 적 사망 처리
        pass

# 게임 실행
game = Game()
game.start()
game.quit() 