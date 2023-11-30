import pygame
import numpy
import math
pygame.init()
from MAVProxy.modules.lib import mp_module
from pymavlink import mavutil


class AttitudeIndicator():
    def __init__(self):
        
        self.__slipAngles = [0,0]
        self.__heading = 0
        self.field_of_view = (30, 30)
        self.ai_size_xy = (400,400)
        self.AIsurf = pygame.Surface(self.ai_size_xy)
        self.sky_colour = (255, 153, 0)
        self.ground_colour = (0, 0, 255)
        self.font1 = pygame.font.SysFont('Arial', 15)

    def getState(self):
        return self.__stateVecs

    def setState(self, pitchNew, rollNew):
        directions = [pygame.math.Vector3(0,0,1), pygame.math.Vector3(0,1,0)]

        pitched = [directions[0].rotate(pitchNew, directions[0].cross(directions[1])), directions[1].rotate(pitchNew, directions[0].cross(directions[1])), directions[1].rotate(pitchNew, directions[0].cross(directions[1]))]
        self.__stateVecs = [pitched[0], pitched[1].rotate(-rollNew, pitched[0]), pitched[1]]


    def getHorizonLine(self, elev, distToHorizon, rollAngle):
        if elev == 0:
            lineLen = [self.ai_size_xy[0]*1.5, self.ai_size_xy[1]*1.5]
        elif elev % 10 == 5:
            lineLen = [self.ai_size_xy[0]*0.15, self.ai_size_xy[1]*0.15]
        else:
            lineLen = [self.ai_size_xy[0]*0.25, self.ai_size_xy[1]*0.25]
        x = self.ai_size_xy[0]//2 + distToHorizon * math.sin(math.radians(rollAngle))
        y = self.ai_size_xy[1]//2 + distToHorizon * math.cos(math.radians(rollAngle))

        #return (x,y)

        lp = [x-lineLen[0]*math.cos(math.radians(-rollAngle)), y-lineLen[1]*math.sin(math.radians(-rollAngle))]
        rp = [x+lineLen[0]*math.cos(math.radians(-rollAngle)), y+lineLen[1]*math.sin(math.radians(-rollAngle))]
        return ([x,y],lp,rp)
            
    def drawAttitudeIndicator(self):
        #self.AIsurf.fill(self.sky_colour)
        self.AIsurf.fill((0,0,0))

        pitchAngle = pygame.math.Vector3(0,0,1).angle_to(self.__stateVecs[0]) if self.__stateVecs[0].z >= 0 else pygame.math.Vector3(0,0,-1).angle_to(self.__stateVecs[0])
        #if self.__stateVecs[0].y < 0:
        #    pitchAngle *= -1

        
        rollAngle = self.__stateVecs[2].angle_to(self.__stateVecs[1])
        ra = rollAngle
        #if self.__stateVecs[1].x < 0:
        #    rollAngle *= -1
        

        

        # center line
        degree_size = [self.ai_size_xy[0]/(self.field_of_view[0]*2), self.ai_size_xy[1]/(self.field_of_view[1]*2)]

        distToHorizon = pitchAngle * degree_size[1]
        horizData = self.getHorizonLine(0, distToHorizon, rollAngle)
        pygame.draw.circle(self.AIsurf, "red", horizData[0], radius=8)
        pygame.draw.line(self.AIsurf, "white", horizData[1], horizData[2], width=4)
        for i in range(-90, 90, 5):
            distToHorizon = (pitchAngle + i) * degree_size[1]
            if i != 0:
                horizData = self.getHorizonLine(i, distToHorizon, rollAngle)
                col = (255, 165, 0) if i>0 else (0,0,255)
                pygame.draw.line(self.AIsurf, col, horizData[1], horizData[2], width=2)
                if i % 10 == 0:
                    self.AIsurf.blit(self.font1.render(str(-i), True, col), horizData[1])

        pygame.draw.circle(self.AIsurf, "white", (self.ai_size_xy[0]//2, self.ai_size_xy[1]//2), radius=5)


        return self.AIsurf


    
print("Running")
conn = mavutil.mavlink_connection("udp:127.0.0.1:14550") # com7   tcp:127.0.0.1:5763
conn.wait_heartbeat()
print("Connected")

m = conn.mav.command_long_encode(
        conn.target_system, conn.target_component,
        511, 0,
        30, # The MAVLink message ID
        50000, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 
        0, 
        0, 
        0, # Unused parameters
        0, # Target address of message stream - 0 default
    ) 

conn.mav.send(m)

response = conn.recv_match(type='COMMAND_ACK', blocking=True)
if response and response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL and response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("Command accepted")
else:
    print("Command failed")
    quit()    


size_xy = (800, 800)
bg_colour = (0,0,0)


DISPLAY = pygame.display.set_mode(size_xy)
CLOCK = pygame.time.Clock()


ai = AttitudeIndicator()


run = True
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False    
    

    m = conn.recv_match(type="ATTITUDE", blocking=True).to_dict()
    ai.setState(m["pitch"]*(180/math.pi), m["roll"]*(180/math.pi))
    s1 = ai.drawAttitudeIndicator()

    

    DISPLAY.blit(s1, (200, 200))

    pygame.display.set_caption(str(round(CLOCK.get_fps(), 2)))
    pygame.display.update()
    DISPLAY.fill(bg_colour)
    CLOCK.tick()
