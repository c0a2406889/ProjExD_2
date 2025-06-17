import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA: dict = {pg.K_UP:[0,-5],
               pg.K_DOWN:[0,5],
               pg.K_LEFT:[-5,0],
               pg.K_RIGHT:[5,0]
}

ALPHA: dict = {
    (0,0):[90,0],
    (0,5):[180,0.9],
    (5,5):[135,0.9],
    (5,0):[90,0.9],
    (5,-5):[45,0.9],
    (0,-5):[0,0.9],
    (-5,-5):[325,0.9],
    (-5,0):[280,0.9],
    (-5,5):[235,0.9],
}


def get_kk_img(kk_img ,sum_mv: tuple[int,int]):
    angle, scale = ALPHA.get(sum_mv, [90, 0.9])
    return pg.transform.rotozoom(kk_img,angle,scale)

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
    gg_txt = fonto.render("Game Over", True, (255, 255, 255))
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
    kk_img_base = pg.image.load("fig/3.png")  
    sum_mv = [0, 0]
    kk_img = get_kk_img(kk_img_base, (0, 0))  
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_speed = init_bb_imgs()
        
    while True:
        sum_mv = [0, 0]

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        new_center = (kk_rct.centerx + sum_mv[0], kk_rct.centery + sum_mv[1])
        new_img = get_kk_img(kk_img_base, tuple(sum_mv))
        new_rct = new_img.get_rect(center=new_center)

        if check_boud(new_rct) == (True, True):
            kk_img = new_img
            kk_rct = new_rct

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 
        screen.blit(kk_img, kk_rct)

        avx = bb_speed[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(vx*avx, vy*avx)
        yoko, tate = check_boud(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
                
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()