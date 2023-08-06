'''

`throws` `nThread` `ext` `nDown`

	>>> throws(f:function,args:tuple)->None
	>>> nThread(
		n:int=16,
		waits:float=0,
		f:function=None,
		args:list=None,
		fast:bool=False,
		)
	>>> ext=dict()
	>>> nDown(
		url:list,
		name:list,
		pth:str,
		h1:list=HEADERS,
		h2:list=HEADERS,
		f:function=None,
		proxies:dict=None,
		stream_size:int=-1,
		chunk_size:int=1<<20,
		n:int=30,
		waits:float=0,
		print_log:bool=True,
		test7z:bool=False,
		)
'''

from downs._thread import throws,nThread
from downs._down import ext,nDown
