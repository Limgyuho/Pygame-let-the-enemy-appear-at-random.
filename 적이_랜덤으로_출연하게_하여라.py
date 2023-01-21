# -*- coding: utf-8 -*-
"""적이 랜덤으로 출연하게 하여라

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fUAXAmNnJWmnuoLn7--6Bkn4B17jmKLH
"""

import pygame
import random

# 1. 초기화 -> 변수 선언
pygame.init()
# 2. 게임 화면 설정 -> 크기 고정
size = [400, 650]
screen = pygame.display.set_mode(size)

title = "PyGameExam"
pygame.display.set_caption(title)

# 3. 게임 화면 내에서의 설정 -> 변수
clock = pygame.time.Clock()


black = (0, 0, 0)

#class로 묶기 
class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    #이미지가 png형식일경우와 아닐경우를 분리한다
    def add_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            
    #어떠한 이미지를 사용하더라도 사이즈가 자동적으로 변하게 해주기 위함이다
    def change_size(self, width, height):
        self.img = pygame.transform.scale(self.img, (width, height))
        self.width, self.height = self.img.get_size()
        
    def show(self):
        screen.blit(self.img, (self.x, self.y))            
#클래스 실행문       
hero = Object()
#클래스 안에 hero에 이미지를 추가한다
hero.add_img("C:\\Users\\USER\\Pictures\\hero2.png")
#hero의 사이즈를 변경할수 있도록 지정해준다
hero.change_size(60,80)
hero.x = round(size[0] / 2) - round(hero.width / 2)
hero.y = size[1] - hero.height - 100
hero.move = 10

left_move = False
right_move = False
space_shot = False

missile_list = []
enemy_list = []

k = 0

# 4. 메인이벤트
system_exit = 0
while(system_exit == 0):
    #  4-1. FPS(Frame per Sec) 설정
    clock.tick(60)
    
    #  4-2. 입력(키보드, 마우스)의 감지

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            system_exit = 1
        #키다운을 계속 누를 경우
        #왼쪽으로 누르면 음의 방향으로
        #오른쪽으로 우르면 양의 방향으로 움직인다 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_move = True
            if event.key == pygame.K_RIGHT:
                right_move = True
            if event.key == pygame.K_SPACE:
                space_shot = True
        #키업과 다운을 분류 해야 되는데 업부분이 if이면
        #빠져나가지 못하여 정상작동이 되지 않는다
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_move = False
            if event.key == pygame.K_RIGHT:
                right_move = False
            if event.key == pygame.K_SPACE:
                space_shot = False
    

    #  4-3. 입력, 시간에 따른 변화
    #위의 키다운 부분에서 왼쪽이냐 오른쪽이냐에 따라
    #아래의 코드가 실행되고 다시 위로 올라가며 무한 반복한다
    #키업을 하면 아래의 코드를 실행하지 않고 가만히 멈추게 된다
    if left_move == True:
        hero.x -= hero.move
        #x좌표의끝은 0이므로 그밑을 벗어나서는 안된다
        #아래의 코드가 위로 간다면 아예 움직이지못하고 넘어가거나
        #조금만 움직이고 아래로 넘어가기 때문이다
        if hero.x<=0:
            hero.x =0
    elif right_move == True:
        hero.x += hero.move 
        #x축을 기준으로 한이유는 통일성을 주기 위함이다
        #siz[]로 한이유는 매번 값이 변경될수 있는 경우를 상정해야 하기 때문이다
        if hero.x >= size[0] - hero.width:
            hero.x = size[0] - hero.width
    if space_shot == True and k % 6 == 0:
        missile = Object()
        missile.add_img("C:\\Users\\USER\Pictures\\missile.png")
        missile.change_size(25, 40)
        missile.x = round(hero.x + hero.width / 2 - missile.width / 2)
        missile.y = hero.y - missile.height - 10
        missile.move = 10
        missile_list.append(missile)
     
    k += 1
    
    delete_list = []
    for i in range(len(missile_list)):
        m = missile_list[i]
        m.y -= m.move
        if m.y <= -m.height:
            delete_list.append(m)
            
    for d in delete_list:  
        missile_list.remove(d)
        
    if random.random() > 0.98:
        #random.random함수는 숫자를 일정 범위에서 무작위로 추출해주는 기능을 준다
        #보통 0부터 1까지 이며 현재는 0.98
        enemy = Object()
        enemy.add_img("C:\\Users\\USER\\Pictures\\enemy1.png")
        enemy.change_size(40,40)
        enemy.x = random.randrange(0,size[1])
        #random.randrange()함수는 랜덤함수의 범위 만큼 사이즈를 지정해준다
        enemy.y = 10
        enemy.move = 1
        enemy_list.append(enemy)
    
    #  4-4. 전사작업(그리기)
    screen.fill(black)
    hero.show()
    for m in missile_list:
        m.show()
        
    for e in enemy_list:
        e.show()

    #  4-5. 업데이트
    pygame.display.flip()

# 5. 종료
pygame.quit()