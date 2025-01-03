from pygame import sprite,transform,time
from random import randint
from setting import H_Width,Hp5_Height,particle_group
class Particle(sprite.Sprite):
	for i in range(10):
			def __init__(self,target):
				super().__init__()
				self.image=transform.scale(target.image,(randint(5,20),randint(5,20)))
				self.rect=self.image.get_rect()
				self.rect.center=H_Width+randint(-50,50),Hp5_Height+target.image_t.get_height()/2+randint(-50,50)
				self.speedx=randint(-10,10)
				self.speedy=randint(20,30)
				self.die_time=0
				self.last_time=time.get_ticks()
				
			def update(self):
				self.die_time=time.get_ticks()-self.last_time
				if self.die_time>1000:
					self.kill()
				self.rect.centerx+=self.speedx
				self.rect.centery+=self.speedy
				
def particle_init(target):
	for i in range(randint(5,15)):
		particle=Particle(target)
		particle_group.add(particle)