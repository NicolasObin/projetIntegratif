#!/usr/bin/env python

class Dance:
	def __init__(self,case):
		if case == 0: #ECOUTE
			self.nbTemps = 1
			self.pos1 = [['HeadPitch', [0.11500812321901321]], ['HeadYaw', [0.49083805084228516]], ['LElbowRoll', [-0.03490658476948738]], ['LElbowYaw', [-1.182755947113037]], ['LShoulderPitch', [1.5293561220169067]], ['LShoulderRoll', [0.28067994117736816]], ['RElbowRoll', [1.5446163415908813]], ['RElbowYaw', [0.007627964019775391]], ['RShoulderPitch', [-1.0691561698913574]], ['RShoulderRoll', [-0.8069260120391846]]]

		elif case == 1: #TOUT ET N IMPORTE QUOI
			self.nbTemps = 3
			self.pos1 = [['HeadPitch', [0.10273600369691849]], ['HeadYaw', [0.08739614486694336]], ['LElbowRoll', [-1.5446163415908813]], ['LElbowYaw', [-0.33905601501464844]], ['LShoulderPitch', [1.1519920825958252]], ['LShoulderRoll', [0.41874003410339355]], ['RElbowRoll', [0.2516179084777832]], ['RElbowYaw', [0.9479701519012451]], ['RShoulderPitch', [1.3008737564086914]], ['RShoulderRoll', [-0.1764519214630127]]]
			self.pos2 = [['HeadPitch', [0.07205605506896973]], ['HeadYaw', [-0.09668397903442383]], ['LElbowRoll', [-0.8789401054382324]], ['LElbowYaw', [-0.658128023147583]], ['LShoulderPitch', [1.1059720516204834]], ['LShoulderRoll', [-0.127363920211792]], ['RElbowRoll', [1.2717280387878418]], ['RElbowYaw', [0.9464361667633057]], ['RShoulderPitch', [1.469614028930664]], ['RShoulderRoll', [0.06131792068481445]]]
			self.pos3 = [['HeadPitch', [0.1288139820098877]], ['HeadYaw', [0.09506607055664062]], ['LElbowRoll', [-0.03490658476948738]], ['LElbowYaw', [-0.9772000312805176]], ['LShoulderPitch', [1.251702070236206]], ['LShoulderRoll', [0.3972640037536621]], ['RElbowRoll', [1.336155891418457]], ['RElbowYaw', [0.7301421165466309]], ['RShoulderPitch', [1.3315539360046387]], ['RShoulderRoll', [-0.015382050536572933]]]

		elif case == 2: #DISCO
			self.nbTemps = 2
			self.pos1 = [['HeadPitch', [0.1058039665222168]], ['HeadYaw', [-0.7240900993347168]], ['LElbowRoll', [-1.3023240566253662]], ['LElbowYaw', [-0.774712085723877]], ['LShoulderPitch', [1.2777800559997559]], ['LShoulderRoll', [0.007627964019775391]], ['RElbowRoll', [0.04452800750732422]], ['RElbowYaw', [0.6503739356994629]], ['RShoulderPitch', [-1.1397199630737305]], ['RShoulderRoll', [-1.0968518257141113]]]
			self.pos2 = [['HeadPitch', [0.1058039665222168]], ['HeadYaw', [-0.7240900993347168]], ['LElbowRoll', [-1.5446163415908813]], ['LElbowYaw', [-1.7135200500488281]], ['LShoulderPitch', [1.971148133277893]], ['LShoulderRoll', [0.07819199562072754]], ['RElbowRoll', [0.04606199264526367]], ['RElbowYaw', [0.6534421443939209]], ['RShoulderPitch', [0.8636841773986816]], ['RShoulderRoll', [0.3141592741012573]]]

		elif case == 3: #SWING
			self.nbTemps = 2
			self.pos1 = [['HeadPitch', [0.12267804145812988]], ['HeadYaw', [-0.29917192459106445]], ['LElbowRoll', [-0.5583341121673584]], ['LElbowYaw', [-1.6705679893493652]], ['LShoulderPitch', [2.0856685638427734]], ['LShoulderRoll', [0.7884340286254883]], ['RElbowRoll', [0.9725980758666992]], ['RElbowYaw', [1.6520761251449585]], ['RShoulderPitch', [1.1014537811279297]], ['RShoulderRoll', [-0.09361600875854492]]]
			self.pos2 = [['HeadPitch', [-0.004643917083740234]], ['HeadYaw', [0.1840381622314453]], ['LElbowRoll', [-1.1289820671081543]], ['LElbowYaw', [-1.619946002960205]], ['LShoulderPitch', [0.6810541152954102]], ['LShoulderRoll', [0.17636799812316895]], ['RElbowRoll', [0.9449858665466309]], ['RElbowYaw', [1.3023240566253662]], ['RShoulderPitch', [1.8086280822753906]], ['RShoulderRoll', [-0.20713186264038086]]]

		elif case == 4: #RAP
			self.nbTemps = 2
			self.pos1 = [['HeadPitch', [0.514872133731842]], ['HeadYaw', [-0.1043538972735405]], ['LElbowRoll', [-0.6580440998077393]], ['LElbowYaw', [-1.1106581687927246]], ['LShoulderPitch', [0.12267804145812988]], ['LShoulderRoll', [0.17023205757141113]], ['RElbowRoll', [0.6734678745269775]], ['RElbowYaw', [-0.3896780014038086]], ['RShoulderPitch', [1.092249870300293]], ['RShoulderRoll', [0.16256213188171387]]]
			self.pos2 = [['HeadPitch', [0.514872133731842]], ['HeadYaw', [-0.1043538972735405]], ['LElbowRoll', [-0.37272000312805176]], ['LElbowYaw', [-1.4573421478271484]], ['LShoulderPitch', [0.9817180633544922]], ['LShoulderRoll', [0.06592011451721191]], ['RElbowRoll', [0.6750020980834961]], ['RElbowYaw', [-0.38814401626586914]], ['RShoulderPitch', [1.1060562133789062]], ['RShoulderRoll', [0.1487560272216797]]]

		elif case == 5: #HIP HOP
			self.nbTemps = 2
			self.pos1 = [['HeadPitch', [0.15642595291137695]], ['HeadYaw', [-0.17184996604919434]], ['LElbowRoll', [-1.1105740070343018]], ['LElbowYaw', [-0.46944594383239746]], ['LShoulderPitch', [-1.055434226989746]], ['LShoulderRoll', [0.7991721630096436]], ['RElbowRoll', [1.5446163415908813]], ['RElbowYaw', [0.8513281345367432]], ['RShoulderPitch', [0.2945699691772461]], ['RShoulderRoll', [-0.21326804161071777]]]
			self.pos2 = [['HeadPitch', [0.18710613250732422]], ['HeadYaw', [-0.17031598091125488]], ['LElbowRoll', [-1.2793140411376953]], ['LElbowYaw', [-1.1137261390686035]], ['LShoulderPitch', [0.8099100589752197]], ['LShoulderRoll', [0.8497941493988037]], ['RElbowRoll', [1.5446163415908813]], ['RElbowYaw', [0.31136012077331543]], ['RShoulderPitch', [0.10128592699766159]], ['RShoulderRoll', [-0.25621986389160156]]]

		elif case == 6: #ROBOT
			self.nbTemps = 3
			self.pos1 = [['HeadPitch', [-0.19792795181274414]], ['HeadYaw', [-0.029187917709350586]], ['LElbowRoll', [-1.4679961204528809]], ['LElbowYaw', [-1.319282054901123]], ['LShoulderPitch', [1.3989660739898682]], ['LShoulderRoll', [-0.23934602737426758]], ['RElbowRoll', [1.4788179397583008]], ['RElbowYaw', [1.5492980480194092]], ['RShoulderPitch', [0.2838320732116699]], ['RShoulderRoll', [0.07512402534484863]]]
			self.pos2 = [['HeadPitch', [-0.19792795181274414]], ['HeadYaw', [-0.029187917709350586]], ['LElbowRoll', [-1.5078800916671753]], ['LElbowYaw', [-1.6214799880981445]], ['LShoulderPitch', [0.14262008666992188]], ['LShoulderRoll', [-0.3141592741012573]], ['RElbowRoll', [1.4205260276794434]], ['RElbowYaw', [1.251702070236206]], ['RShoulderPitch', [1.569324016571045]], ['RShoulderRoll', [0.27761197090148926]]]
			self.pos3 = [['HeadPitch', [-0.19792795181274414]], ['HeadYaw', [-0.02611994743347168]], ['LElbowRoll', [-1.4526560306549072]], ['LElbowYaw', [-1.6107420921325684]], ['LShoulderPitch', [1.440384030342102]], ['LShoulderRoll', [-0.23934602737426758]], ['RElbowRoll', [1.5202360153198242]], ['RElbowYaw', [1.3744220733642578]], ['RShoulderPitch', [0.21940398216247559]], ['RShoulderRoll', [0.23619413375854492]]]

