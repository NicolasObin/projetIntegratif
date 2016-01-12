
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
		subprocess.call(["scp",filename,"nao@"+IP+":"+storage])
		print "Ordi -> NAO"
		print filename
		subprocess.call(["sshpass","-p","'nao'","scp",ordiname,"nao@"+IP+":"+storage])
		print outname
	else:	
		#print "NAO -> Ordi"
		print "outname = "+outname
		print "ordiname = "+ordiname
		
		#subprocess.call(["scp","nao@"+IP+":"+outname,ordidir])

		subprocess.call(["sshpass","-p",'nao',"scp","nao@"+IP+":"+outname,ordiname])
		print ordiname

	return [outname,ordiname]


	
