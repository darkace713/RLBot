import math

'''
Description: TBD
'''

# Username: Darkace713
# Contact Email:
# Can this bot's code be shared publicly: No
# Can non-tournment gameplay of this bot be displayed publicly (Default: No):

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


class agent:
	#turn = 16383 #Joystick X pos 0=left
	
	def __init__(self, team): #Constructor
		self.team = team
		
	def get_bot_name(self):
		# This is the name that will be displayed on screen in the real time display!
		return "TestAgent001"

	def get_output_vector(self, input):
		#Get ball info
		ball_x = input[0][7] #Ball x position
		ball_y = input[0][6] #Ball y position
		ball_z = input[0][2] #Ball z position
		ball_vx = input[0][31] #Ball X Velocity
		ball_vy = input[0][32] #Ball Y Velocity
		ball_vz = input[0][33] #Ball Z Velocity
		
		#Zeroize bot inputs (TODO make a function) ####################
		turn = 16383

		#Get bots info
		if (self.team == "blue"):
			player_x = input[0][5] #Blue X Position
			player_y = input[0][4] #Blue Y Position
			player_z = input[0][1] #Blue Z Position
			player_vx = input[0][28] #Blue X Velocity
			player_vy = input[0][29] #Blue Y Velocity
			player_vz = input[0][30] #Blue Z Velocity
			player_rot1 = input[0][8]
			player_rot2 = input[0][9]
			player_rot3 = input[0][10]
			player_rot4 = input[0][11]
			player_rot5 = input[0][12]
			player_rot6 = input[0][13]
			player_rot7 = input[0][14]
			player_rot8 = input[0][15]
			player_rot9 = input[0][16]
		else:
			player_x = input[0][18] #Orange X Position
			player_y = input[0][17]	#Orange Y Position
			player_z = input[0][3] #Orange Z Position
			player_rot1 = input[0][19]
			player_rot2 = input[0][20]
			player_rot3 = input[0][21]
			player_rot4 = input[0][22]
			player_rot5 = input[0][23]
			player_rot6 = input[0][24]
			player_rot7 = input[0][25]
			player_rot8 = input[0][26]
			player_rot9 = input[0][27]
		

		
		# Need to handle atan2(0,0) case, aka straight up or down, eventually
		player_front_direction_in_radians = math.atan2(player_rot1, player_rot4)
		relative_angle_to_ball_in_radians = math.atan2((ball_x - player_x), (ball_z - player_z))

		#TEMP make bot front flip into ball
		ball_dist = ((player_x - ball_x)**2 + (player_y - ball_y)**2 + (player_z - ball_z)**2)**0.5
		
		if (not (abs(player_front_direction_in_radians - relative_angle_to_ball_in_radians) < math.pi)):
			# Add 2pi to negative values
			if (player_front_direction_in_radians < 0):
				player_front_direction_in_radians += 2 * math.pi
			if (relative_angle_to_ball_in_radians < 0):
				relative_angle_to_ball_in_radians += 2 * math.pi

		if (relative_angle_to_ball_in_radians > player_front_direction_in_radians):
			turn = 0
		else:
			turn = 32767
			
		#LJoyX, LJoyY, FWDAccel, BCKAccel, JMP1|0, BST1|0, DRFT1|0
		#0L 32767R, 0B 32767F, 32676FullSpeed
		return [turn, 16383, 32767, 0, 2, 0, 0]
