import threading
import time

def throws(f,args:tuple=tuple())->None:
	if not isinstance(args,tuple):
		args=(args,)
	_t=threading.Thread(target=f,args=args)
	_t.setDaemon(True)
	_t.start()
	return _t

class nThread:
	def __init__(
		self,
		n:int=16,
		waits:int=0,
		f=None,
		args:list=None,
		fast:bool=False,
	):
		self.__ed=False
		self.__q=list()
		
		self.__n=len(args) if fast else n
		self.__total=0
		self.__finish=0
		
		self.__waits=waits
		self.__mian=throws(self.__f)
		if fast:
			self.ths(f,args)
			self.join()

	def __repr__(self):
		_d={
			'classname':'nThread',
			'waittime':self.__waits,
			'total':self.__total,
			'finished':self.__finish,
			'limited':self.__n,
			'running':min(self.__n,len(self.__q)),
			'waiting':len(self.__q)-self.__n,
		}
		return _d

	def __str__(self):
		return '<class nThread with '+str(self.__n)+' threads>'

	def __del__(self):
		print('del this class nThread; '+str(self.__finish)+'/'+str(self.__total)+' threads are finished')

	def __f(self):
		_l=list()
		while True:
			if self.__ed and not len(_l):
				return
			for i in _l.copy():
				if not i.is_alive():
					_l.remove(i)
					self.__finish+=1
			while len(self.__q)>0 and len(_l)<self.__n:
				f,args=self.__q.pop(0)
				if not isinstance(args,tuple):
					args=(args,)
				if self.__waits:
					time.sleep(self.__waits)
				_l.append(throws(f,args))
	
	def th(self,f,args:tuple=tuple()):
		self.__total+=1
		self.__q.append((f,args,))

	def thl(self,l:list):
		self.__total+=len(l)
		self.__q+=l

	def ths(self,f,l:list):
		if isinstance(l,int):
			l=list(range(l))
		self.__total+=len(l)
		self.__q+=[(f,i,) for i in l]

	def join(self):
		self.__ed=True
		self.__mian.join()
		self.__ed=False
