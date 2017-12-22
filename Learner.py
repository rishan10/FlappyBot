from City import Game
import time
import json





class FlappyBot:
	World = Game()

	World.init() ##open website

	qvalues = {}

	actions = World.actions

	state = ""

	dead = None

	gameCNT = 0 # Game count of current run, incremented after every death
	DUMPING_N = 25 # Number of iterations to dump Q values to JSON after
	discount = 1.0

	lr = 0.7
	last_state = "14_0_5"
	last_action = 0
	moves = []


	def load_qvalues(self):
	        '''
	        Load q values from a JSON file
	        '''
	        self.qvalues = {}
	        try:
	            fil = open('qvalues.json', 'r')
	        except IOError:
	            return
	        self.qvalues = json.load(fil)
	        fil.close()

	def map_state(self,mx, my, by):
		return str(mx)+'_'+str(my)+'_'+str(by)

	def act(self,mx, my, by):
	        '''
	        Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
	        '''
	        self.state = self.map_state(mx, my, by)

	        self.moves.append( [self.last_state, self.last_action, self.state] ) # Add the experience to the history

	        self.last_state = self.state # Update the last_state with the current state

	        if self.qvalues[self.state][0] >= self.qvalues[self.state][1]:
	        	self.last_action = 0
	        	return 0
	        else:
	        	self.last_action = 1
	        	self.World.flap()
	        	return 1


	def update_scores(self):
	        '''
	        Update qvalues via iterating over experiences
	        '''
	        history = list(reversed(self.moves))

	        #Q-learning score updates

	        scoreIncreased = self.World.scoreIncreased()
	        dead = self.World.playerIsDead()
	        tooHigh = self.World.driver.execute_script('return bird.y') <= (self.World.driver.execute_script('return counter.y')-150)

	        for exp in history:
	            state = exp[0]
	            act = exp[1]
	            res_state = exp[2]
	            if (not dead) and (scoreIncreased):
	                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * (1 + (self.discount)*max(self.qvalues[res_state]) )

	            elif dead or tooHigh:
	                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * (-10 + (self.discount)*max(self.qvalues[res_state]))

	            else:
	                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * (0.1 + (self.discount)*max(self.qvalues[res_state]))
	            

	        self.gameCNT += 1 #increase game count
	        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
	        if(len(self.moves) >= 3): 
	        	self.moves = []  #clear history after updating strategies


	def dump_qvalues(self):
	        '''
	        Dump the qvalues to the JSON file
	        '''
	        if self.gameCNT % self.DUMPING_N == 0:
	            fil = open('qvalues.json', 'w')
	            json.dump(self.qvalues, fil)
	            fil.close()
	            print('Q-values updated on local file.')



	def run(self):
		gameNotStarted = True
		self.load_qvalues()
	
		while True:
				if not self.World.closeableAdIsPlaying():
					if not self.World.videoAdIsPlaying():

						try:
							dead = self.World.playerIsDead()
						except Exception as e:
							print("page hasn't loaded yet!")


						if(dead!=None):
							if not dead:
								
								if gameNotStarted:
									self.World.flap()
									gameNotStarted = False


								birdy = int(self.World.getYBirdLocation())/100
								try:
									midptX = int(self.World.getPipeXMidPoint())/100
								except Exception as e:
									midptX = 14

								try:
									midptY = int(self.World.getPipeYMidPoint())/100
								except Exception as e:
									midptY = 0

								self.act(midptX, midptY, birdy)

								self.update_scores()
								

							else:
								self.update_scores()
								time.sleep(0.7)
								self.World.hitRestart()
								gameNotStarted = True
				else:
					self.World.getRidOfClosaebleAd()
				




		self.World.quit()
