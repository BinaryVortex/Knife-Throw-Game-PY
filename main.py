from pygame import init,FINGERDOWN,FINGERMOTION,FINGERUP,gfxdraw,transform,BLEND_RGBA_MULT
init()
from random import randint
from os import walk
from setting import *
from circle import Circle
from knife import Knife
from particle import particle_init
from stage import Stage
from value import *
class Game:
	def __init__(self):
		#game variable
		self.on=1
		self.lose=0
		self.rest_time=0
		self.last_time=0
		self.boss_fight=0
		self.current_stage=1
		self.stage=Stage(self.current_stage)
		self.stage.boss_init()
		self.delta_time=60
		#knife setup
		self.knife_path=knife_storage.current_dict["imgs"]
		#circle setup
		self.circle=Circle("wood0.png")
		circle_group.add(self.circle)
		#currency
		self.apple_value=apple_value
		
	def respawn_knife(self):
		if self.lose!=1:
			if self.stage.health!=0:
				if len(knife_group)==0:
					knife=Knife(knife_storage.current_knife)
					knife_group.add(knife)
		
	def throw_knife(self):
		if len(knife_group)>0:
			knife_group.sprites()[0].is_throw=1
			throw_sound.play()
	
	def knife_collision(self):
		if len(knife_group)>0:
			if knife_group.sprites()[0].is_hit==1:
				for kni in knife_hit_group.sprites():
					if kni.angle<10 or kni.angle>350:
						self.lose=1
						break
				if self.lose!=1:
					for apple in apple_group.sprites():
						if apple.angle<20 or apple.angle>340:
							apple.is_sliced=1
							apple.angle=180
							slice_sound.play()
							self.apple_value+=2
							particle_init(apple)

		if self.lose==1:
			if self.last_time==0:
				self.last_time=time.get_ticks()
				knife_hit_sound.play()
			self.rest_time=time.get_ticks()-self.last_time
			if self.rest_time>1000:
				self.last_time=0
				knife_group.empty()
				knife_hit_group.empty()
				apple_group.empty()
				circle_group.empty()
				self.lose=0
				self.stage.boss_init()
				self.current_stage=1
				self.stage.__init__(self.current_stage)
				self.on=0
				restart_menu.on=1
				
	def knife_hit(self):
		if self.lose!=1:
			if len(knife_group)>0:
				if knife_group.sprites()[0].is_hit==1:
					knife_hit_group.add(knife_group.sprites()[0])
					knife_group.empty()
					
					particle_init(self.circle)
					
					self.stage.health-=1
					screen.blit(hit_effect,(H_Width-hit_effect.get_width()/2,Hp5_Height-hit_effect.get_height()/2))
					self.circle.get_hit()
		
	def circle_respawn(self):
		if self.lose!=1:
			if self.stage.health==0:
				if self.last_time==0:
					self.last_time=time.get_ticks()
					self.circle.break_sound.play()
					
				self.rest_time=time.get_ticks()-self.last_time
				if self.rest_time>1000:
					self.last_time=0
					
					knife_group.empty()
					knife_hit_group.empty()
					
					apple_group.empty()
					
					self.current_stage+=1
					self.stage.__init__(self.current_stage)
					
					circle_group.empty()
		if len(circle_group)==0:
			self.circle=Circle(f"wood{self.current_stage//5}.png") if self.current_stage%5!=0 else Circle(self.stage.boss_name)
			circle_group.add(self.circle)
		
	def draw(self):
		if self.stage.current%5!=0:	
			for i in range(4):
				gfxdraw.circle(screen,H_Width-75+i*50,300,10,bright_blue)
			for i in range(self.current_stage%5):
				gfxdraw.filled_circle(screen,H_Width-75+i*50,300,10,bright_blue)
			cre_text_center(f"Stage: {self.stage.current}",H_Width,400,60,bright_blue)
		else:
			screen.blit(boss_icon,(H_Width-boss_icon.get_width()/2,300))
			boss_name=self.stage.boss_name.replace(".png","")
			cre_text_center(boss_name,H_Width,450,100,(250,100,0))
			
		for i in range(self.stage.health):
			screen.blit(knife_icon,(100,1600-i*50))
		
		cre_text_center(self.apple_value,Width-150,65,50,orange)
		screen.blit(apple_icon,(Width-100,20))
		
		knife_group.draw(screen)
		knife_hit_group.draw(screen)
		particle_group.draw(screen)
		circle_group.draw(screen)
		apple_group.draw(screen)
		
	def handle_event(self):
		self.throw_knife()
	
	def run(self):
		self.stage.update()
		self.draw()
		
		circle_group.update(self.stage.angular_vel,self.stage.health,self.delta_time)
		self.circle_respawn()
		
		self.respawn_knife()
		self.knife_collision()
		self.knife_hit()
		knife_group.update(self.stage.angular_vel,self.stage.health,self.lose,self.delta_time)
		knife_hit_group.update(self.stage.angular_vel,self.stage.health,self.lose,self.delta_time)
		
		particle_group.update()
		apple_group.update(self.stage.angular_vel,self.stage.health,self.delta_time)
		
	def loop(self):
		while self.on:
			clock.tick(60)
			self.delta_time=60/clock.get_fps()
			screen.blit(bg,(0,0))
			for ev in fastevent.get():
				if ev.type==FINGERDOWN:
					self.handle_event()
			self.run()
			display.update()

class Knife_storage:
	def __init__(self):
		self.on=1
		self.menu_icon_posx=0
		self.menu_icon_posy=0
		
		self.random_icon_posx=H_Width-random_icon.get_width()/2
		self.random_icon_posy=2000-random_icon.get_height()/2
		
		self.fxd,self.fy=0,0
		self.fx=0
		self.slide_posx=0
		self.is_slide=0
		self.select_index=0
		
		self.imgs_sizey=230
		self.imgs_scale_speed=1
		self.arc_angle0=0
		self.arc_angle1=180
		
		def import_knife_folder(folder,unlock,buyable):
			for _,__,img in walk(folder):
				break
			imgs=[image.load(folder+i).convert_alpha() for i in img]
			imgs_icon=[transform.rotate(imgs[i],-45).convert_alpha() for i in range(len(imgs))]
			knife_pos=[[(Width-imgs_icon[i].get_width()*4)/2+i%4*imgs_icon[i].get_width(),1000+i//4*imgs_icon[i].get_height()] for i in range(len(imgs))]
			return {"imgs":imgs,"imgs_icon":imgs_icon,"knife_pos":knife_pos,"unlock":unlock,"buyable":buyable}
			
		dict0=import_knife_folder("knifes0/",knife_storage0_unlock,knife_storage0_buyable)
		
		dict1=import_knife_folder("knifes1/",knife_storage1_unlock,knife_storage1_buyable)
		
		self.list=[dict0,dict1]
		self.list_index=0
		self.current_dict=self.list[self.list_index]
		self.speed=0
		self.is_unlock=0
		self.current_knife=dict0["imgs"][0]
		
	def loop(self):
		while self.on:
			clock.tick(60)
			#handle event
			for ev in fastevent.get():
				if ev.type==FINGERDOWN:
					self.fxd,self.fy=ev.x*Width,ev.y*Height
					if self.menu_icon_posx<self.fxd<self.menu_icon_posx+menu_icon.get_width() and self.menu_icon_posy<self.fy<self.menu_icon_posy+menu_icon.get_height():
						self.on=0
					if self.current_dict["buyable"]==1:
						if self.random_icon_posx<self.fxd<self.random_icon_posx+random_icon.get_width() and self.random_icon_posy<self.fy<self.random_icon_posy+random_icon.get_height():
							if 0 in self.current_dict["unlock"]:
								if game.apple_value>=50:
									game.apple_value-=50
									self.is_unlock=1
						
					for i in range(len(self.current_dict["imgs_icon"])):
						if self.current_dict["knife_pos"][i][0]<self.fxd<self.current_dict["knife_pos"][i][0]+self.current_dict["imgs_icon"][0].get_width() and self.current_dict["knife_pos"][i][1]<self.fy<self.current_dict["knife_pos"][i][1]+self.current_dict["imgs_icon"][0].get_height():
							self.select_index=i
							if self.current_dict["unlock"][self.select_index]==1:
							 self.current_knife=self.current_dict["imgs"][self.select_index]
							 
				self.is_slide=1 if ev.type==FINGERDOWN or ev.type==FINGERMOTION else 0
				if self.is_slide==1:
					self.fx=ev.x*Width
					self.slide_posx=self.fx-self.fxd

			if self.is_slide==0:
				if self.slide_posx<0:
					self.slide_posx+=20
				if self.slide_posx>0:
					self.slide_posx-=20
					
			if self.slide_posx<-H_Width and self.list_index!=len(self.list)-1:
				self.select_index=0
				self.list_index+=1
			
			if self.slide_posx>H_Width and self.list_index!=0:
				self.select_index=0
				self.list_index-=1
				
			self.current_dict=self.list[self.list_index]
			#random
			max_speed=randint(20,30)/10
			if self.is_unlock==1:
				self.select_index+=int(self.speed)
				self.speed+=0.01
				if self.speed>max_speed:
					self.speed=0
					self.is_unlock=0
					
				if self.select_index>=len(self.current_dict["imgs"]):
					self.select_index=0
				
				if 0 in self.current_dict["unlock"]:
					for i in range(len(self.current_dict["unlock"])-1):
						if self.current_dict["unlock"][self.select_index]==1:
							self.select_index+=1
							if self.select_index>=len(self.current_dict["imgs"]):
								self.select_index=0

				if self.speed==0:
					self.current_dict["unlock"][self.select_index]=1
				
			#draw
			screen.blit(bg_dark_green,(0,0))
			screen.blit(menu_icon,(self.menu_icon_posx,self.menu_icon_posy))
			gfxdraw.filled_circle(screen,H_Width,600,300,(90,140,140))
			gfxdraw.arc(screen,H_Width,600,300,self.arc_angle0,self.arc_angle0+90,bright_blue_green)
			gfxdraw.arc(screen,H_Width,600,250,self.arc_angle1,self.arc_angle1+90,bright_blue_green)
			gfxdraw.arc(screen,H_Width,600,200,self.arc_angle0,self.arc_angle1+90,bright_blue_green)
			self.arc_angle0+=1
			self.arc_angle1-=2
			#show img
			self.imgs_sizey-=self.imgs_scale_speed
			if self.imgs_sizey<=200 or self.imgs_sizey>=230:
				self.imgs_scale_speed*=-1
			
			show_imgs=transform.scale(self.current_dict["imgs"][self.select_index],(45,self.imgs_sizey)).copy()
			if self.current_dict["unlock"][self.select_index]==0:
				show_imgs.fill((0,0,0,200),None,BLEND_RGBA_MULT)
			
			screen.blit(show_imgs,(H_Width-show_imgs.get_width()/2,600-show_imgs.get_height()/2))
			#shiny effect
			screen.blit(shiny_effect,(H_Width-shiny_effect.get_width()/2,600-shiny_effect.get_height()/2))
			
			#img icon bg
			gfxdraw.box(screen,(self.current_dict["knife_pos"][self.select_index][0]+self.slide_posx,self.current_dict["knife_pos"][self.select_index][1],self.current_dict["imgs_icon"][0].get_width(),self.current_dict["imgs_icon"][0].get_height()),medium_blue_green)
			#img icon
			for i in range(len(self.current_dict["imgs_icon"])):
				
				gfxdraw.rectangle(screen,(self.current_dict["knife_pos"][i][0]+self.slide_posx,self.current_dict["knife_pos"][i][1],self.current_dict["imgs_icon"][i].get_width(),self.current_dict["imgs_icon"][i].get_height()),(50,100,100))
				
				imgs_icon=self.current_dict["imgs_icon"][i]
				if self.current_dict["unlock"][i]==0:
					imgs_icon=self.current_dict["imgs_icon"][i].copy()
					imgs_icon.fill((0,0,0,200),None,BLEND_RGBA_MULT)
					
				screen.blit(imgs_icon,(self.current_dict["knife_pos"][i][0]+self.slide_posx,self.current_dict["knife_pos"][i][1]))
			
			cre_text_center(game.apple_value,Width-150,65,50,orange)
			screen.blit(apple_icon,(Width-100,20))
			
			if self.current_dict["buyable"]==1:
				screen.blit(random_icon,(self.random_icon_posx,self.random_icon_posy))
			#strorage index
			gap=50
			for i in range(len(self.list)):
				gfxdraw.circle(screen,H_Width-gap*(i-len(self.list)//2+1)+gap//2,1800,10,bright_blue_green)
			gfxdraw.filled_circle(screen,H_Width-(gap*len(self.list))//2+gap//2+self.list_index*gap,1800,10,bright_blue_green)
			display.update()

class Option:
	def __init__(self):
		self.on=1
		self.menu_icon_posx=0
		self.menu_icon_posy=0
		self.fx,self.fy=0,0
		
		self.sound_posx=100
		self.sound_posy=800
		self.sound_button_posx=1000
		self.sound_button_posy=1000
		self.sound_is_adjust=0
		
		self.sfx_posx=100
		self.sfx_posy=1200
		self.sfx_button_posx=1000
		self.sfx_button_posy=1400
		self.sfx_is_adjust=0
		
	def loop(self):
		while self.on:
			clock.tick(60)
			#handle event
			for ev in fastevent.get():
				if ev.type==FINGERDOWN or ev.type==FINGERMOTION:
					self.fx,self.fy=ev.x*Width,ev.y*Height
					
					if self.sound_posx<=self.fx<=self.sound_posx+900 and self.sfx_is_adjust==0:
						if self.sound_button_posx-100<self.fx<self.sound_button_posx+100 and self.sound_button_posy-100<self.fy<self.sound_button_posy+100:
						 	self.sound_is_adjust=1
						if self.sound_is_adjust==1:
							self.sound_button_posx=int(self.fx)
							bg_sound.set_volume((self.sound_button_posx-100)/1000)
					
					if self.sfx_posx<=self.fx<=self.sfx_posx+900 and self.sound_is_adjust==0:
						if self.sfx_button_posx-100<self.fx<self.sfx_button_posx+100 and self.sfx_button_posy-100<self.fy<self.sfx_button_posy+100:
							self.sfx_is_adjust=1
						if self.sfx_is_adjust==1:
							self.sfx_button_posx=int(self.fx)
							throw_sound.set_volume((self.sfx_button_posx-100)/1000)
							knife_hit_sound.set_volume((self.sfx_button_posx-100)/1000)
							for i in wood_hit_sound:
								i.set_volume((self.sfx_button_posx-100)/1000)
							wood_broke_sound.set_volume((self.sfx_button_posx-100)/1000)
							slice_sound.set_volume((self.sfx_button_posx-100)/1000)
					if self.menu_icon_posx<self.fx<self.menu_icon_posx+menu_icon.get_width() and self.menu_icon_posy<self.fy<self.menu_icon_posy+menu_icon.get_height():
						self.on=0
				if ev.type==FINGERUP:
					self.sound_is_adjust=0
					self.sfx_is_adjust=0
			#draw		
			screen.blit(bg_dark_green,(0,0))
			
			screen.blit(menu_icon,(self.menu_icon_posx,self.menu_icon_posy))
			
			cre_text("Sound",self.sound_posx,self.sound_posy,100,bright_blue_green)
			gfxdraw.circle(screen,100,self.sound_button_posy,20,bright_blue_green)
			gfxdraw.line(screen,self.sound_posx,self.sound_button_posy,self.sound_button_posx,self.sound_button_posy,bright_blue_green)
			gfxdraw.filled_circle(screen,self.sound_button_posx,self.sound_button_posy,20,bright_blue_green)
			gfxdraw.circle(screen,1000,self.sound_button_posy,20,bright_blue_green)
			
			cre_text("Sfx",self.sfx_posx,self.sfx_posy,100,bright_blue_green)
			gfxdraw.circle(screen,100,self.sfx_button_posy,20,bright_blue_green)
			gfxdraw.line(screen,self.sfx_posx,self.sfx_button_posy,self.sfx_button_posx,self.sfx_button_posy,bright_blue_green)
			gfxdraw.filled_circle(screen,self.sfx_button_posx,self.sfx_button_posy,20,bright_blue_green)
			gfxdraw.circle(screen,1000,self.sfx_button_posy,20,bright_blue_green)
			display.update()			

class Restart_menu:
	def __init__(self):
		self.on=1
		self.restart_icon_posx=H_Width-restart_icon.get_width()/2
		self.restart_icon_posy=1600-restart_icon.get_height()/2
		
		self.knife_storage_icon_posx=H_Width-knife_storage_icon.get_width()/2-250
		self.knife_storage_icon_posy=1600-knife_storage_icon.get_height()/2
		
		self.option_icon_posx=H_Width-option_icon.get_width()/2+250
		self.option_icon_posy=1600-option_icon.get_height()/2
		
		self.menu_icon_posx=0
		self.menu_icon_posy=0
		
	def loop(self):
		while self.on:
			clock.tick(60)
			#handle event
			for ev in fastevent.get():
				if ev.type==FINGERDOWN:
					fx,fy=ev.x*Width,ev.y*Height
					if self.restart_icon_posx<fx<self.restart_icon_posx+restart_icon.get_width() and self.restart_icon_posy<fy<self.restart_icon_posy+restart_icon.get_height():
						game.on=1
						game.loop()
					
					if self.knife_storage_icon_posx<fx<self.knife_storage_icon_posx+knife_storage_icon.get_width() and self.knife_storage_icon_posy<fy<self.knife_storage_icon_posy+knife_storage_icon.get_height():
						knife_storage.on=1
						knife_storage.loop()
						
					if self.option_icon_posx<fx<self.option_icon_posx+option_icon.get_width() and self.option_icon_posy<fy<self.option_icon_posy+option_icon.get_height():
						option.on=1
						option.loop()
						
					if self.menu_icon_posx<fx<self.menu_icon_posx+menu_icon.get_width() and self.menu_icon_posy<fy<self.menu_icon_posy+menu_icon.get_height():
						self.on=0
			
			#draw
			screen.blit(bg_dark,(0,0))
			
			screen.blit(restart_icon,(self.restart_icon_posx,self.restart_icon_posy))
			
			screen.blit(knife_storage_icon,(self.knife_storage_icon_posx,self.knife_storage_icon_posy))
			
			screen.blit(option_icon,(self.option_icon_posx,self.option_icon_posy))
			
			screen.blit(menu_icon,(self.menu_icon_posx,self.menu_icon_posy))
			
			display.update()

class Menu:
	def __init__(self):
		self.on=1
		self.play_icon_posx=H_Width-play_icon.get_width()/2
		self.play_icon_posy=1200-play_icon.get_height()/2
		
		self.option_icon_posx=H_Width-option_icon.get_width()/2
		self.option_icon_posy=1400-option_icon.get_height()/2
		
		self.knife_storage_icon_posx=H_Width-knife_storage_icon.get_width()/2
		self.knife_storage_icon_posy=1600-knife_storage_icon.get_height()/2
		
		self.exit_icon_posx=0
		self.exit_icon_posy=0
		
	def loop(self):
		while self.on:
			clock.tick(60)
			#handle event
			for ev in fastevent.get():
				if ev.type==FINGERDOWN:
					fx,fy=ev.x*Width,ev.y*Height
					if self.play_icon_posx<fx<self.play_icon_posx+play_icon.get_width() and self.play_icon_posy<fy<self.play_icon_posy+play_icon.get_height():
						game.on=1
						game.loop()
						
					if self.option_icon_posx<fx<self.option_icon_posx+option_icon.get_width() and self.option_icon_posy<fy<self.option_icon_posy+option_icon.get_height():
						option.on=1
						option.loop()
					
					if self.knife_storage_icon_posx<fx<self.knife_storage_icon_posx+knife_storage_icon.get_width() and self.knife_storage_icon_posy<fy<self.knife_storage_icon_posy+knife_storage_icon.get_height():
						knife_storage.on=1
						knife_storage.loop()
					
					if self.exit_icon_posx<fx<self.exit_icon_posx+exit_icon.get_width() and self.exit_icon_posy<fy<self.exit_icon_posy+exit_icon.get_height():
						self.on=0
		
			if game.on==0:
				restart_menu.loop()
				
			#draw		
			screen.blit(bg,(0,0))

			cre_title_center("Knife",540,300,200,bright_blue)
			cre_title_center("Hit",540,550,200,bright_blue)
			
			cre_text_center(game.apple_value,Width-150,65,50,orange)
			screen.blit(apple_icon,(Width-100,20))
			
			screen.blit(play_icon,(self.play_icon_posx,self.play_icon_posy))
			
			screen.blit(option_icon,(self.option_icon_posx,self.option_icon_posy))
			
			screen.blit(knife_storage_icon,(self.knife_storage_icon_posx,self.knife_storage_icon_posy))
			
			screen.blit(exit_icon,(self.exit_icon_posx,self.exit_icon_posy))
			
			display.update()
			
option=Option()
knife_storage=Knife_storage()
game=Game()
restart_menu=Restart_menu()
menu=Menu()			
menu.loop()
file=open("value.py","w")
def file_write(name,var):
	file.write(f"{name}={var}\n")
	
file_write("apple_value",game.apple_value)
file_write("knife_storage0_unlock",knife_storage.list[0]['unlock'])
file_write("knife_storage1_unlock",knife_storage.list[1]['unlock'])
file_write("all_boss_unlock",[knife_storage.list[1]['unlock']])
file_write("knife_storage0_buyable",1)
file_write("knife_storage1_buyable",0)