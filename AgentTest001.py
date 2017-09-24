from enum import Enum
import math, time

'''
Description: TBD
'''

# Username: Darkace713
# Contact Email:
# Can this bot's code be shared publicly: No
# Can non-tournment gameplay of this bot be displayed publicly (Default: No):

#Enum to know what the bot is currently doing
class Status(Enum):
	STAT_DUMB = 0
	STAT_FLIP_FRONT_0 = 10
	STAT_FLIP_FRONT_01 = 101
	STAT_FLIP_FRONT_1 = 11
	STAT_FLIP_FRONT_2 = 12
	STAT_FLIP_FRONT_3 = 13

##TODO make a queue for input commands
class CommandQueue:
	class Command:
		def __init__(self):
			self.something = 0

	def __init__(self):
		self.commands = []
		self.numCommands = 0

	def add(self, command):
		self.commands.append(command)



''' Input table
input[0][0] | Blue Boost | Amount of boost blue has [0-100]
input[0][1] | Blue Z | Z is about -120 back of blue goal, -100 blue goal line, 0 for midfield, 100 orange goal line, 120 back orange goal. Blue Z is the Z position of the blue car.
input[0][2] | Ball Z | (See Blue Z)
input[0][3] | Orange Z | (See Blue Z)
input[0][4] | Blue Y | About 0 for ground, about 40 for ceiling.
input[0][5] | Blue X | -82 for right wall when facing orange goal, 82 for left wall facing orange goal.  0 is middle of goal.
input[0][6] | Ball Y | (See Blue Y)
input[0][7] | Ball X | (See Blue X)
input[0][8] | Blue Rot1 | 1 when front of car pointing towards positive x, 0 when front of car facing z direction, -1 when facing -x direction.  Angles in between filled in.
input[0][9] | Blue Rot2 | Same as Rot4 but when upside down 1 and -1 switched.
input[0][10] | Blue Rot3 | Bottom of wheels facing ground/ceiling = 0.  Wheels facing -x = 1, wheels facing +x = -1
input[0][11] | Blue Rot4 | 1 when front of car facing positive z, -1 when facing negative z, 0 when facing + or - x.
input[0][12] | Blue Rot5 | Same as Rot1 except when upside down 1 and -1 switched.
input[0][13] | Blue Rot6 | Wheels facing -z = 1, wheels facing +z = -1, wheels on ground / ceiling = 0
input[0][14] | Blue Rot7 | Car nose facing up = 1, car nose facing down = -1, car on ground/ceiling = 0
input[0][15] | Blue Rot8 | Wheels +x and nose +z = -1, wheels +x and nose -z = 1, wheels -x and nose +z = 1, wheels -x and nose -z = -1
input[0][16] | Blue Rot9 | Wheels on ground = 1, wheels facing ceiling = -1, wheels on wall = 0
input[0][17] | Orange Y | (See Blue Y)
input[0][18] | Orange X | (See Blue X)
input[0][19] | Orange Rot1 | (See Rotation values above)
input[0][20] | Orange Rot2 | (See Rotation values above)
input[0][21] | Orange Rot3 | (See Rotation values above)
input[0][22] | Orange Rot4 | (See Rotation values above)
input[0][23] | Orange Rot5 | (See Rotation values above)
input[0][24] | Orange Rot6 | (See Rotation values above)
input[0][25] | Orange Rot7 | (See Rotation values above)
input[0][26] | Orange Rot8 | (See Rotation values above)
input[0][27] | Orange Rot9 | (See Rotation values above)
input[0][28] | Blue X Velocity
input[0][29] | Blue Y Velocity
input[0][30] | Blue Z Velocity
input[0][31] | Ball X Velocity
input[0][32] | Ball Y Velocity
input[0][33] | Ball Z Velocity
input[0][34] | Orange X Vel
input[0][35] | Orange Y Vel
input[0][36] | Orange Z Vel
input[0][37] | Orange Boost | Amount of boost orange has [0-100]

input[1][0] | Blue Score | Actually scoreboard score for blue team
input[1][1] | Orange Score | Actually scoreboard score for orange team
input[1][2] | Orange Demos | Demos on Blue and by Orange
input[1][3] | Blue Demos | Demos on Orange and by Blue
input[1][4] | Blue Points | Like points for first touch, center ball, etc for blue
input[1][5] | Orange points | Like points for first touch, center ball, etc for orange
input[1][6] | Blue Goals | Goals by blue (If blue never touches the ball and it goes in this would not increment which blue score does)
input[1][7] | Blue Saves | Saves by Blue
input[1][8] | Blue Shots | Shots by Blue
input[1][9] | Orange Goals | Goals by Orange
input[1][10] | Orange Saves | Saves by Orange
input[1][11] | Orange Shots | Shots by Orange
'''


JOY_ZERO = 16383 #Center joystick for "no input"
JOY_LEFT = 0 #Hold joystick all the way left
JOY_RIGHT = 32767 #Hold joystick all the way right
JOY_UP = 0 #Hold joystick all the way up
JOY_DOWN = 32767 #Hold joystick all the way down
MAX_THROTTLE = 32767
MIN_THROTTLE = 0

class agent:
	def __init__(self, team): #Constructor
		self.team = team
		self.status = Status.STAT_DUMB  # enum to know cars current state
		self.out_vector = [16383, 16383, 32767, 0, 0, 0, 0]
		self.XJoy = JOY_ZERO
		self.YJoy = JOY_ZERO

		self.ballPos = [0,0,0] #Ball x,y,z position
		self.ballVel = [0,0,0] #Ball x,y,z velocity

		self.pos = [0,0,0] #Player x,y,z position
		self.vel = [0,0,0] #Player x,y,z velocity
		self.rot = [[0,0,0], [0,0,0], [0,0,0]] #Something something rotation idk

	def get_bot_name(self): #Return name to be displayed
		return "TestAgent001"
	
	def Reset_inputs(self):
		self.out_vector = [JOY_ZERO, JOY_ZERO, MAX_THROTTLE, 0, 0, 0, 0]
		return

	#Calculates the distance between two 3 element position arrays
	def GetDistance(self, t1, t2):
		return ( ((t1[0] - t2[0])**2) + ((t1[1] - t2[1])**2) + ((t1[2] - t2[2])**2) )**0.5

	#Used to turn the car left/right ## TODO make this better
	def UpdateXJoy(self, angle_to_ball, player_direction):
		#print("angle_to_ball: " + str(angle_to_ball) + " player_direction: " + str(player_direction))
		if (angle_to_ball > player_direction):
			self.out_vector[0] = JOY_LEFT
		else:
			self.out_vector[0] = JOY_RIGHT
		return self.out_vector
		
	#Outputs to perform a front flip
	def FrontFlip(self):
		#YJoy down + jump, YJoy down + jump again, wait til something?
		if (self.status == Status.STAT_FLIP_FRONT_0):
			self.out_vector = [JOY_ZERO, JOY_UP, MAX_THROTTLE, 0, 1, 0, 0] #Tilt down and jump
			self.status = Status.STAT_FLIP_FRONT_1 #Set next state
		#elif (self.status == Status.STAT_FLIP_FRONT_01): #TODO test hold keys longer
		#	self.out_vector = [JOY_ZERO, JOY_UP, MAX_THROTTLE, 0, 1, 0, 0]  # Tilt down and jump
		#	self.status = Status.STAT_FLIP_FRONT_1  # Set next state
		elif (self.status == Status.STAT_FLIP_FRONT_1):
			self.out_vector = [JOY_ZERO, JOY_UP, MAX_THROTTLE, 0, 0, 0, 0] #Tilt down and release jump
			self.status = Status.STAT_FLIP_FRONT_2 #Set next state
		elif (self.status == Status.STAT_FLIP_FRONT_2):
			self.out_vector = [JOY_ZERO, JOY_UP, MAX_THROTTLE, 0, 1, 0, 0] #Tilt down and jump again
			self.status = Status.STAT_FLIP_FRONT_3 #Set next state
		elif (self.status == Status.STAT_FLIP_FRONT_3): #Front flip complete, release buttons
			self.out_vector = [JOY_ZERO, JOY_ZERO, MAX_THROTTLE, 0, 0, 0, 0]
			self.status = Status.STAT_DUMB #Set next state
		return self.out_vector

	#Main function for the agent
	def get_output_vector(self, input):
		#Initialize bot inputs (so if one is not updated it is released/centered)
		self.Reset_inputs()
		
		#Get ball info
		self.ballPos = [input[0][7], input[0][6], input[0][2]]
		self.ballVel = [input[0][31], input[0][32], input[0][33]]
		
		#Get the bot's info
		if (self.team == "blue"):
			self.pos = [input[0][5], input[0][4], input[0][1]]
			self.vel = [input[0][28], input[0][29], input[0][30]]
			self.rot = [[input[0][8], input[0][9], input[0][10]],
						[input[0][11], input[0][12], input[0][13]],
						[input[0][14], input[0][15], input[0][16]]]
		else: #Orang team
			self.pos = [input[0][18], input[0][17], input[0][3]]
			self.vel = [input[0][34], input[0][35], input[0][36]]
			self.rot = [[input[0][19], input[0][20], input[0][21]],
						[input[0][22], input[0][23], input[0][24]],
						[input[0][25], input[0][26], input[0][27]]]
		

		# Need to handle atan2(0,0) case, aka straight up or down, eventually
		player_direction = math.atan2(self.rot[0][0], self.rot[1][0])
		angle_to_ball = math.atan2((self.ballPos[0] - self.pos[0]), (self.ballPos[2] - self.pos[2]))

		ball_dist = self.GetDistance(self.pos, self.ballPos)

		if (not (abs(player_direction - angle_to_ball) < math.pi)):
			# Add 2pi to negative values
			if (player_direction < 0):
				player_direction += 2 * math.pi
			if (angle_to_ball < 0):
				angle_to_ball += 2 * math.pi

		#determine next action
		if ((ball_dist < 10) and (self.status == Status.STAT_DUMB)):  # do front flip if near ball
			self.status = Status.STAT_FLIP_FRONT_0
			
		if (self.status == Status.STAT_DUMB):
			self.out_vector = self.UpdateXJoy(angle_to_ball, player_direction)
		else:
			self.FrontFlip()
			
		#LJoyX, LJoyY, FWDAccel, BCKAccel, JMP1|0, BST1|0, DRFT1|0
		#0L 32767R, 0U 32767D, 32676FullSpeed
		#return [JOY_ZERO, JOY_ZERO, MAX_THROTTLE, 0, 0, 1, 0]
		return self.out_vector

		
		
		
		