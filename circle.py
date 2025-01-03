from pygame import sprite,image,transform
from math import atan2,sin,cos
from random import choice,randint
from setting import screen,H_Width,Hp5_Height,wood_hit_sound,wood_broke_sound
class Circle(sprite.Sprite):
			def __init__(self,img_name):
				super().__init__()
				self.image=image.load(img_name).convert_alpha()
				self.image_t=self.image
				self.rect=self.image.get_rect()
				self.rect.center=H_Width,Hp5_Height
				self.angle=0
				self.hit_sound=wood_hit_sound
				self.break_sound=wood_broke_sound
				#piece
				part=20//choice((2,4,5))
				self.part_speed=15
				
				self.part=[self.image_t.subsurface(
				i,j,self.image_t.get_width()//part,self.image_t.get_height()//part
				) for i in range(0,self.image_t.get_width(),self.image_t.get_width()//part) for j in range(0,self.image_t.get_height(),self.image_t.get_height()//part)]
				
				self.part_pos=[[
				H_Width-self.image_t.get_width()/2+i*self.image_t.get_width()//part,
				Hp5_Height-self.image_t.get_height()/2+j*self.image_t.get_height()//part
				]
				for i in range(part) for j in range(part)]
				self.part_angle=[0 for i in range(len(self.part))]
				
				self.dir_part_angle=[-atan2(self.part_pos[i][0]-H_Width,self.part_pos[i][1]-Hp5_Height) for i in range(len(self.part))]
				
			def rotate(self):
				self.image=transform.rotate(self.image_t,self.angle)
				
				circle_half_size=200
				self.rect.centerx=H_Width+circle_half_size-self.image.get_width()/2
				self.rect.centery=Hp5_Height+circle_half_size-self.image.get_height()/2
				
			def get_hit(self):
				self.rect.centery-=20
				self.hit_sound[randint(0,4)].play()
				
			def broken(self,delta_time):
				self.image=transform.scale(self.image_t,(0,0))
				for i in range(len(self.part)):
					screen.blit(transform.rotate(self.part[i],self.part_angle[i]),(self.part_pos[i][0],self.part_pos[i][1]))
					
					self.part_pos[i][0]-=self.part_speed*sin(self.dir_part_angle[i])
					self.part_pos[i][1]+=self.part_speed*cos(self.dir_part_angle[i])
					
					self.part_angle[i]+=20*delta_time
				self.part_speed+=1*delta_time
					
			def update(self,angular_vel,health,delta_time):
				self.angle+=angular_vel*delta_time
				if health!=0:
					self.rotate()
				else:
					self.broken(delta_time)