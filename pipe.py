import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, img, top):
        super().__init__()
        self.image = img
        # rect 是把指定圖片框起來，就定位好圖片的上下左右等等位置
        self.rect = self.image.get_rect()
        self.speedx = 4
        self.last_pic_time = pygame.time.get_ticks()
        self.img_frequency = 1500
        self.bird_pass = False
        if top:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)


    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.kill() ##Sprite裡面的方法，做刪除




