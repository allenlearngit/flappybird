## flappy bird
import pygame
import random
from  bird import Bird
from pipe import Pipe
pygame.init()

def generate_pipes(last_pipe_time, pipe_frequency, pipe_group):
    now = pygame.time.get_ticks()
    if now - last_pipe_time >= pipe_frequency:
        random_height = random.randint(-100, 100)
        pipe_btm = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + pipe_gap / 2 + random_height, pipe_img, False)
        pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 - pipe_gap / 2 + random_height, flip_pipe_img, True)
        pipe_group.add(pipe_top)
        pipe_group.add(pipe_btm)
        return  now
    return last_pipe_time

def draw_score():
    # 顯示的文字要轉成字串
    score_text = score_font.render(str(score), True, WHITE)
    window.blit(score_text, (SCREEN_WIDTH/2-score_text.get_width()/2, 20))


##設定常數
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)


##邊框設置
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("可愛的鳥鳥")
clock = pygame.time.Clock()


###導入圖片
#背景
bg_img = pygame.image.load("img/bg.png")
##下方修改圖片的大小，在設置一個同名稱變數可以蓋過去
bg_img = pygame.transform.scale(bg_img, (780, 600))
#鳥
bird_imgs = []
for i in range(1, 3):
    bird_imgs.append(pygame.image.load(f"img/bird{i}.png"))
##換視窗的標題小圖
pygame.display.set_icon(bird_imgs[0])
##地板
ground_img = pygame.image.load("img/ground.png")
##水管
pipe_img = pygame.image.load("img/pipe.png")
flip_pipe_img = pygame.transform.flip(pipe_img, False, True)
##重新開始
restart_img = pygame.image.load("img/restart.png")


#載入字體
score_font = pygame.font.Font("微軟正黑體.ttf", 60) #字體路徑 字體大小


#遊戲變數
ground_speed = 4
ground_x = 0
pipe_gap = 150
pipe_frequency = 1500
last_pipe_time = pygame.time.get_ticks() - pipe_frequency
ground_top = SCREEN_HEIGHT - 100
game_over = False
score = 0

bird = Bird(100, SCREEN_HEIGHT/2, bird_imgs)
bird_group = pygame.sprite.Group()#創建群組物件
bird_group.add(bird)#把鳥加進去群組


#將水管圖片加入群組，不能寫在函式內，因為下面迴圈要使用
pipe_group = pygame.sprite.Group()


##遊戲內容
run = True
while run: #沒有mainloop的方式，必須自己寫迴圈讓畫面一直顯示
    clock.tick(FPS) #限制該迴圈一秒鐘內最多執行的次數
    # ---取得輸入---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                bird.jump()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                last_pipe_time = pygame.time.get_ticks() - pipe_frequency
                bird.reset()
                ##第一種刪除管子的寫法
                # for pipe in pipe_group.sprites():
                #     pipe.kill()
                ##第二種刪除管子的寫法
                pipe_group.empty()

    # ---更新遊戲---
    bird_group.update(ground_top)
    if not game_over:
        pipe_group.update()
        last_pipe_time = generate_pipes(last_pipe_time, pipe_frequency, pipe_group)
        # 判斷是否通過管子 sprites 會回傳列表 可以取得群組裡面的所有物件
        first_pipe = pipe_group.sprites()[0] #第一根水管
        # 將群組在設定成一個變數，再套用類別裡的屬性
        if not first_pipe.bird_pass:
            if first_pipe.rect.right < bird.rect.left:
                score += 1
                first_pipe.bird_pass = True

        #移動地板
        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0
    #碰撞判斷
    #下方後面可以不用加 == {}，直接寫會回傳{}等於Flase
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or\
        bird.rect.top <= 0 or\
        bird.rect.bottom >= ground_top:
        game_over = True
        bird.game_over()


    # ---畫面顯示---
    window.blit(bg_img, (0, 0))
    bird_group.draw(window)
    pipe_group.draw(window)
    draw_score()
    if game_over:
        window.blit(restart_img, (SCREEN_WIDTH/2-restart_img.get_width()/2, SCREEN_HEIGHT/2-restart_img.get_height()/2))
    window.blit(ground_img, (ground_x, ground_top))
    pygame.display.update()

pygame.quit()
