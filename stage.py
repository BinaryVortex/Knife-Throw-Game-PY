from pygame import image
from knife import Knife
from apple import Apple
from setting import knife_hit_group,apple_group
from random import randint,choices
from value import knife_storage1_unlock
def obstacle_knife(angle):
	knife=Knife(image.load("knifes0/k0.png").convert_alpha())
	knife.is_hit=1
	knife.angle=angle
	knife_hit_group.add(knife)
def apple_init(angle):
	apple=Apple()
	apple.angle=angle
	apple_group.add(apple)
class Stage:
	def __init__(self,current):
		self.current=current
		self.change_direction=0
		#round0
		if self.current==1:
			n=0#randint(0,2)
			if n==0:
				apple_init(randint(0,340))
			self.lvl_init(3,8,None)
		if self.current==2:
			n=randint(0,2)
			if n==0:
				apple_init(randint(70,290))
			obstacle_knife(310)
			obstacle_knife(50)
			self.lvl_init(-2,10,None)
		if self.current==3:
			n=randint(0,2)
			if n==0:
				apple_init(randint(20,100))
			obstacle_knife(0)
			obstacle_knife(120)
			obstacle_knife(240)
			self.lvl_init(0,8,self.rot_stop)
			self.rot_stop_parameter=(0,4,0.05)
		if self.current==4:
			n=randint(0,2)
			if n==0:
				apple_init(randint(20,340))
			obstacle_knife(0)
			self.lvl_init(0,10,self.rot_stop)
			self.rot_stop_parameter=(-5,0,0.05)
		#round1
		if self.current==6:
			n=randint(0,2)
			if n==0:
				apple_init(randint(70,340))
			obstacle_knife(50)
			self.lvl_init(2,10,self.rot_stop)
			self.rot_stop_parameter=(-5,5,0.04)
		if self.current==7:
			n=randint(0,2)
			if n==0:
				apple_init(randint(0,290))
			obstacle_knife(310)
			self.lvl_init(2,10,self.rot_stop)
			self.rot_stop_parameter=(-4,4,0.02)
		if self.current==8:
			n=randint(0,2)
			if n==0:
				apple_init(randint(20,160))
			obstacle_knife(0)
			obstacle_knife(180)
			self.lvl_init(2,12,self.rot_stop)
			self.rot_stop_parameter=(-4,0,0.04)
		if self.current==9:
			n=randint(0,2)
			if n==0:
				apple_init(randint(200,340))
			obstacle_knife(90)
			obstacle_knife(180)
			self.lvl_init(-2.7,12,None)
		#round2
		if self.current==11:
			n=randint(0,2)
			if n==0:
				apple_init(randint(0,160))
			obstacle_knife(180)
			self.lvl_init(2,12,self.rot_stop)
			self.rot_stop_parameter=(-4,0,0.06)
		if self.current==12:
			n=randint(0,2)
			if n==0:
				apple_init(randint(0,340))
			self.lvl_init(5,10,self.rot_stop)
			self.rot_stop_parameter=(-0,8,0.08)
		if self.current==13:
			n=randint(0,2)
			if n==0:
				apple_init(randint(20,340))
			obstacle_knife(0)
			self.lvl_init(0,8,self.rot_stop)
			self.rot_stop_parameter=(-8,8,0.08)
		if self.current==14:
			n=randint(0,2)
			if n==0:
				apple_init(randint(120,340))
			obstacle_knife(0)
			obstacle_knife(100)
			self.lvl_init(-8,10,self.rot_stop)
			self.rot_stop_parameter=(-8,8,0.05)
		#boss
		if self.current%5==0:
			self.boss_name=choices(tuple(self.boss_dict.keys()),tuple(self.boss_dict.values()),k=1)[0]
			if self.boss_name=="rock.png":
				self.lvl_init(2.5,14,None)
			if self.boss_name=="orange.png":
				for i in range(4):
					apple_init(i*90)
				self.lvl_init(-3.5,12,None)
			if self.boss_name=="pixel.png":
				self.lvl_init(0,10,self.rot_stop)
				self.rot_stop_parameter=(0,8,0.1)
				
	def boss_init(self):
		self.boss_dict={"rock.png":1,"orange.png":1,"pixel.png":1}
		
	def lvl_init(self,angular_v,health,lvl):
		self.angular_vel=angular_v
		self.health=health
		self.stage=lvl if lvl!=None else None
		
	def rot_stop(self,para):
		#para
		#[0]:min angular vel
		#[1]:max angular vel
		#[2]:speed
		if self.angular_vel<=para[0]:
			self.change_direction=0
		if self.angular_vel>=para[1]:
			self.change_direction=1
		self.angular_vel+=para[2] if self.change_direction==0 else -para[2]
		
	def update(self):
		if self.stage!=None:
			self.stage(self.rot_stop_parameter)
		if self.current%5==0:
			if self.health==0:
				if self.boss_name in self.boss_dict:
					knife_storage1_unlock[list(self.boss_dict.keys()).index(self.boss_name)]=1
					self.boss_dict.pop(self.boss_name)