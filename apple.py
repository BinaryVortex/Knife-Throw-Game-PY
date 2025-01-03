from pygame import sprite,transform
from setting import H_Width,Hp5_Height,Height,screen,apple_img,apple_piece0,apple_piece1
from math import sin,cos,radians
from random import randint
class Apple(sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=transform.rotate(apple_img,180)
		self.image_t=self.image
		self.rect=self.image.get_rect()
		self.rect.center=-500,-500
		self.angle=0
		self.is_sliced=0
		#piece
		self.part0_speedx=0
		self.part0_speedy=randint(1,2)
		self.part1_speedx=0
		self.part1_speedy=randint(1,2)
		
		self.accelatey0=randint(18,22)/10
		self.accelatey1=randint(18,22)/10
		self.part=[apple_piece0,apple_piece1]
		self.part_angle=randint(-30,30)

	def rotate(self):
		self.image=transform.rotate(self.image_t,self.angle)
		
		circle_half_size=200
		apple_half_size=50
				
		self.rect.centerx=H_Width+(circle_half_size+25)*sin(radians(self.angle))-self.image.get_width()/2+apple_half_size
				
		self.rect.centery=Hp5_Height+(circle_half_size+25)*cos(radians(self.angle))-self.image.get_height()/2+apple_half_size
		
		if self.angle>360:
			self.angle=0
		if self.angle<0:
			self.angle=360
			
	def get_sliced(self,angular_vel,delta_time):
		
		if self.part0_speedx==0:
			apple_half_size=50
			self.part_pos=[[self.rect.centerx-apple_half_size,self.rect.centery-apple_half_size],[self.rect.centerx-apple_half_size,self.rect.centery-apple_half_size]]
			self.image=transform.scale(self.image,(0,0))
			
		for i in range(len(self.part)):
			screen.blit(self.part[i],self.part_pos[i])
			if self.part_pos[0][1]>Height and self.part_pos[1][1]>Height:
				self.kill()
				
		self.part_pos[0][0]+=self.part0_speedx
		self.part_pos[0][1]+=self.part0_speedy
		self.part_pos[1][0]+=self.part1_speedx
		self.part_pos[1][1]+=self.part1_speedy
		
		self.part0_speedx=angular_vel*delta_time
		self.part1_speedx=angular_vel*delta_time
		
		self.part0_speedy+=self.accelatey0*delta_time
		self.part1_speedy+=self.accelatey1*delta_time
		
	def fly_away(self,delta_time):
		if self.part0_speedx==0:
			apple_half_size=50
			self.part_pos=[[self.rect.centerx-apple_half_size,self.rect.centery-apple_half_size],[self.rect.centerx-apple_half_size,self.rect.centery-apple_half_size]]
		self.rect.centery+=self.part0_speedy
		self.part0_speedy+=2*delta_time
		if self.part_pos[0][1]>Height and self.part_pos[1][1]>Height:
			self.kill()
			
	def update(self,angular_vel,health,delta_time):
		if self.is_sliced==1:
			self.get_sliced(angular_vel,delta_time)
		elif health>0:
			self.angle+=angular_vel*delta_time
			self.rotate()
		if health<=0:
			self.fly_away(delta_time)