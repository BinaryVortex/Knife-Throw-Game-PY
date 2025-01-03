from pygame import sprite,image,transform
from setting import H_Width,Hp5_Height
from math import atan2,sin,cos,radians
from random import randint
class Knife(sprite.Sprite):
		def __init__(self,img):
			super().__init__()
			self.image=img
			self.image_t=self.image
			self.rect=self.image.get_rect()
			self.rect.center=H_Width,1600
			self.angle=0
			self.is_throw=0
			self.is_hit=0
			self.speed=10
			self.fly_speed=randint(30,60)
					
		def hit(self,delta_time):
			distance=self.rect.centery-(Hp5_Height)
			if distance<self.image.get_height():
				self.is_hit=1
			if self.is_hit!=1:
				if self.is_throw==1:
					self.speed+=20*delta_time
					self.rect.centery-=self.speed
			else:
				if self.angle>360:
					self.angle=0
				if self.angle<0:
					self.angle=360
				self.image=transform.rotate(self.image_t,self.angle)
				circle_half_size=200
				knife_half_width=22.5
				knife_half_height=117.5
				
				self.rect.centerx=H_Width+circle_half_size*sin(radians(self.angle))-self.image.get_width()/2+knife_half_width
				
				self.rect.centery=Hp5_Height+circle_half_size*cos(radians(self.angle))-self.image.get_height()/2+knife_half_height
			
		def fly_away(self,delta_time):
			dir_angle=-atan2(self.rect.centerx-H_Width,self.rect.centery-Hp5_Height)
			
			self.rect.centerx-=self.fly_speed*sin(dir_angle)
			self.rect.centery+=self.fly_speed*cos(dir_angle)
			self.fly_speed+=5*delta_time
			
			self.image=transform.rotate(self.image_t,(self.angle))
			
			self.angle+=30*delta_time
					
		def update(self,angular_vel,health,lose,delta_time):
			if self.is_hit==1:
				self.angle+=angular_vel*delta_time
			if health!=0 and lose!=1:
				self.hit(delta_time)
			else:
				self.fly_away(delta_time)