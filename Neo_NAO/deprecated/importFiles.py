
import subprocess
import os

def command_scp(filename,ordidir,dest,IP):
# filename -> absolute path to "toto.wav"
# True -> nao / False -> ordi 
		
	[head,tail] = os.path.split(filename)
	storage = "/home/nao/recordings/"
	outname = storage+tail
	ordiname = ordidir+tail
	if dest == True:
#		subprocess.call(["scp",filename,"nao@"+IP+":"+outname])
		subprocess.call(["sshpass","-p","'nao'","scp",filename,"nao@"+IP+":"+outname])
	else:	
		subprocess.call(["scp","nao@"+IP+":"+outname,ordiname])
#		subprocess.call(["sshpass","-p","'nao'","scp","nao@"+IP+":"+outname,ordiname])

	return [outname,ordiname]


	
