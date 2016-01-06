import subprocess
import os

def command_scp(filename,ordidir):
# filename -> absolute path to "toto.wav"
# True -> nao / False -> ordi 
		
	[head,tail] = os.path.split(filename)
	storage = "/home/nao/recordings/"
	outname = storage+tail
	ordiname = ordidir+tail
	if dest == True:
		subprocess.call(["scp",filename,"nao@127.0.0.1:"+outname])
		print 'nao'
