from pygame import display,font,fastevent,time,image,mixer,sprite,transform
# screen
Width=1080
Height=2290
H_Width=Width//2
H_Height=Height//2
Hp5_Height=Height/2.5
screen=display.set_mode((Width,Height))
# color
medium_blue_green=(100,150,150)
bright_blue=(0,150,250)
bright_blue_green=(200,250,250)
orange=(255,185,75)
#font & text
def cre_text(name,x,y,size,color):
	f=font.Font(None,size)
	t=f.render(str(name),1,color).convert_alpha()
	screen.blit(t,(x,y))
def cre_text_center(name,x,y,size,color):
	f=font.Font(None,size)
	t=f.render(str(name),1,color).convert_alpha()
	screen.blit(t,(x-t.get_width()/2,y-t.get_height()/2))
def cre_title_center(name,x,y,size,color):
	f=font.Font("eddie.ttf",size)
	t=f.render(str(name),1,color).convert_alpha()
	screen.blit(t,(x-t.get_width()/2,y-t.get_height()/2))
#event
fastevent.init()
#time
clock=time.Clock()
#image
bg=image.load("bg.png").convert()
bg_dark=image.load("bg_dark.png").convert()
bg_dark_green=image.load("bg_dark_green.png").convert()
hit_effect=image.load("hit_effect.png").convert_alpha()

boss_icon=image.load("boss.png").convert_alpha()

play_icon=image.load("play_icon.png").convert_alpha()
option_icon=image.load("option_icon.png").convert_alpha()
menu_icon=image.load("menu_icon.png").convert_alpha()
exit_icon=image.load("exit_icon.png").convert_alpha()
restart_icon=image.load("restart_icon.png").convert_alpha()

knife_icon=image.load("knife_icon.png").convert_alpha()

knife_storage_icon=image.load("knife_storage_icon.png").convert_alpha()
shiny_effect=image.load("shiny_effect.png").convert_alpha()
random_icon=image.load("random_icon.png").convert_alpha()

apple_img=image.load("apple.png").convert_alpha()
apple_icon=transform.scale(image.load("apple_piece0.png"),(70,70)).convert_alpha()
apple_piece0=transform.rotate(image.load("apple_piece0.png"),180).convert_alpha()
apple_piece1=transform.rotate(image.load("apple_piece1.png"),180).convert_alpha()

#sound
bg_sound=mixer.Sound("bg.mp3")
#bg_sound.play(-1)
throw_sound=mixer.Sound("throw.mp3")
knife_hit_sound=mixer.Sound("knife_hit.mp3")
wood_hit_sound=[mixer.Sound(f"hit{i}.mp3") for i in range(5)]
wood_broke_sound=mixer.Sound("broken.mp3")
slice_sound=mixer.Sound("slice.mp3")
#sprite group
circle_group=sprite.Group()

knife_group=sprite.GroupSingle()
knife_hit_group=sprite.Group()

particle_group=sprite.Group()

apple_group=sprite.Group()