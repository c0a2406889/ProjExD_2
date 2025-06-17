import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA: dict = {pg.K_UP:[0,-5],pg.K_DOWN:[0,5],pg.K_LEFT:[-5,0],pg.K_RIGHT:[5,0]}
ALPHA: dict = {(-5,-5):[0.25,0.09]}
KK_IMGS = {}

def get_kk_img(sum_mv: tuple[int,int]):
    return pg.transform.rotozoom(pg.image.load("fig/3.png"), ALPHA[sum_mv])

def check_boud(rct: pg.Rect):
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向の画面内が判定結果
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate


def init_bb_imgs():
    bb_accs = [a for a in range(1,11)]
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    
    return bb_imgs,bb_accs


def gameover(screen: pg.Surface):
    gg_img = pg.Surface((1100,650))
    gg_img.set_alpha(100)
    fonto = pg.font.Font(None,80)
    gg_txt = fonto.render("GAME OVER", True, (255, 255, 255))
    gg_txt_rect = gg_txt.get_rect()
    gg_txt_rect.center = (WIDTH/2,HEIGHT/2)
    naki_kk = pg.image.load("fig/8.png")
    naki_kk_rect1 = naki_kk.get_rect(center=(350, HEIGHT / 2))
    naki_kk_rect2 = naki_kk.get_rect(center=(750, HEIGHT / 2))
    pg.draw.rect(gg_img,(0,0,0),pg.Rect(0,0,1100,650))
    screen.blit(gg_img,(0,0))
    screen.blit(naki_kk,naki_kk_rect1)
    screen.blit(gg_txt,gg_txt_rect)
    screen.blit(naki_kk,naki_kk_rect2)
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_speed = init_bb_imgs()

    
    while True:
        avx = bb_speed[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500,9)]
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_boud(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx*avx,vy*avx)
        yoko,tate = check_boud(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        print(bb_img.get_rect())
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()