import os, sys

import time
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare senvironment variable 'SUMO_HOME'")
    
import traci
import traci.constants
import csv

def getTrafficLightPhaseDurations(trafficLightID):
    prog1 = 45, 5, 10
    prog2 = 30, 5, 25
    prog3 = 60, 5, 25
    prog4 = 45, 5, 40
    if trafficLightID[-1] == '1':
            return prog1
    elif trafficLightID[-1] == '2':
            return prog2
    elif trafficLightID[-1] == '3':
            return prog3
    elif trafficLightID[-1] == '4':
            return prog4
            
def getTrafficLightProgramIDs():
    
    #traffic light programs' IDs
    trafficLight1Prog1 = "ramp1_tl_program1"
    trafficLight1Prog2 = "ramp1_tl_program2"
    trafficLight1Prog3 = "ramp1_tl_program3"
    trafficLight1Prog4 = "ramp1_tl_program4"
    trafficLight2Prog1 = "ramp2_tl_program1"
    trafficLight2Prog2 = "ramp2_tl_program2"
    trafficLight2Prog3 = "ramp2_tl_program3"
    trafficLight2Prog4 = "ramp2_tl_program4"
    trafficLight3Prog1 = "ramp3_tl_program1"
    trafficLight3Prog2 = "ramp3_tl_program2"
    trafficLight3Prog3 = "ramp3_tl_program3"
    trafficLight3Prog4 = "ramp3_tl_program4"

    trafficLightProgs = [[trafficLight1Prog1, trafficLight1Prog2, trafficLight1Prog3, trafficLight1Prog4],
                         [trafficLight2Prog1, trafficLight2Prog2, trafficLight2Prog3, trafficLight2Prog4],
                         [trafficLight3Prog1, trafficLight3Prog2, trafficLight3Prog3, trafficLight3Prog4]]
    return trafficLightProgs

## sumoBinary = os.sep+"usr"+os.sep+"bin"+os.sep+"sumo-gui"
## Linux: sumoBinary = "/usr/bin/sumo-gui" but nicer as: sumoBinary = os.sep+"usr"+os.sep+"bin"+os.sep+"sumo-gui"
## Win: sumoBinary = "C:\\Sumo\\bin\\sumo-gui.exe" but nicer as: sumoBinary = "C:"+os.sep+"Sumo"+os.sep+"bin"+os.sep+"sumo-gui.exe"
## sumoBinary = "C:"+os.sep+"Sumo"+os.sep+"bin"+os.sep+"sumo.exe"
## sumoCmd = [sumoBinary, "-c", "autonomous.sumocfg", "--start"]
sumoCmd = ["sumo-gui", "-c", "autonomous.sumocfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

#traffic lights' IDs
trafficLight1 = "TL_0"
trafficLight2 = "TL_1"
trafficLight3 = "TL_2"

trafficLightProgs = getTrafficLightProgramIDs()

print("Program TL1: ", traci.trafficlight.getProgram(trafficLight1))
print("Program TL2: ", traci.trafficlight.getProgram(trafficLight2))
print("Program TL3: ", traci.trafficlight.getProgram(trafficLight3))

# Init
step = 1
tl1_prog = 0
tl2_prog = 0
tl3_prog = 0
# Flow [veh/h] 200 [veh/h] -> 1 veh / 60 min (3600 sec) -> 3600 / vehicle/hour
hw_vph = 400
scale = 1
ramp1_vph = 200
ramp2_vph = 200
ramp3_vph = 200

car_num_ramp1 = 0
car_num_ramp2 = 0
car_num_ramp3 = 0

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Program TL1 green', 'Program TL1 yellow','Program TL1 red',
                     'Program TL2 green', 'Program TL2 yellow','Program TL2 red',
                     'Program TL3 green', 'Program TL3 yellow','Program TL3 red',
                     'Highway Flow [veh/h]', 'Ramp1 Flow [veh/h]',
                     'Ramp2 Flow [veh/h]', 'Ramp3 Flow [veh/h]',
                     'hwLoop10MeanSpeed',
                     'hwLoop10VehicleNum',
                     'hwLoop11MeanSpeed',
                     'hwLoop11VehicleNum',
                     'hwLoop20MeanSpeed',
                     'hwLoop20VehicleNum',
                     'hwLoop21MeanSpeed',
                     'hwLoop21VehicleNum',
                     'hwLoop30MeanSpeed',
                     'hwLoop30VehicleNum',
                     'hwLoop31MeanSpeed',
                     'hwLoop31VehicleNum',
                     'hwLoop40MeanSpeed',
                     'hwLoop40VehicleNum',
                     'hwLoop41MeanSpeed',
                     'hwLoop41VehicleNum',
                     'rampLoop1MeanSpeed',
                     'rampLoop1VehicleNum',
                     'rampLoop2MeanSpeed',
                     'rampLoop2VehicleNum',
                     'rampLoop3MeanSpeed',
                     'rampLoop3VehicleNum'])

random.seed(510)

while step < 600000:
	# this runs one simulation step
    traci.simulationStep()
    
    if (step % 600) == 0: # every 10 min....
        tl1_prog = random.randint(0, 3)
        tl2_prog = random.randint(0, 3)
        tl3_prog = random.randint(0, 3)
        traci.trafficlight.setProgram(trafficLight1, trafficLightProgs[0][tl1_prog])
        traci.trafficlight.setProgram(trafficLight2, trafficLightProgs[1][tl2_prog])
        traci.trafficlight.setProgram(trafficLight3, trafficLightProgs[2][tl3_prog])
        
        hwLoop40MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop40")
        hwLoop41MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop41")
        hwLoop40VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop40")
        hwLoop41VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop41")
        hwLoop30MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop30")
        hwLoop31MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop31")
        hwLoop30VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop30")
        hwLoop31VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop31")
        hwLoop20MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop20")
        hwLoop21MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop21")
        hwLoop20VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop20")
        hwLoop21VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop21")
        hwLoop10MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop10")
        hwLoop11MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("hwLoop11")
        hwLoop10VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop10")
        hwLoop11VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("hwLoop11")
        
        rampLoop1MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("rampLoop1")
        rampLoop1VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("rampLoop1")
        rampLoop2MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("rampLoop2")
        rampLoop2VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("rampLoop2")
        rampLoop3MeanSpeed = traci.inductionloop.getLastIntervalMeanSpeed("rampLoop3")
        rampLoop3VehicleNum = traci.inductionloop.getLastIntervalVehicleNumber("rampLoop3")
   
        with open('output.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_NONE, escapechar=',')
            writer.writerow([getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight1))[0],
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight1))[1],
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight1))[2],
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight2))[0], 
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight2))[1], 
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight2))[2], 
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight3))[0],
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight3))[1],
                             getTrafficLightPhaseDurations(traci.trafficlight.getProgram(trafficLight3))[2],
                             hw_vph * scale,
                             ramp1_vph,
                             ramp2_vph,
                             ramp3_vph,
                             hwLoop10MeanSpeed,
                             round(hwLoop10VehicleNum / 10 * 60),
                             hwLoop11MeanSpeed,
                             round(hwLoop11VehicleNum / 10 * 60),
                             hwLoop20MeanSpeed,
                             round(hwLoop20VehicleNum / 10 * 60),
                             hwLoop21MeanSpeed,
                             round(hwLoop21VehicleNum / 10 * 60),
                             hwLoop30MeanSpeed,
                             round(hwLoop30VehicleNum / 10 * 60),
                             hwLoop31MeanSpeed,
                             round(hwLoop31VehicleNum / 10 * 60),
                             hwLoop40MeanSpeed,
                             round(hwLoop40VehicleNum / 10 * 60),
                             hwLoop41MeanSpeed,
                             round(hwLoop41VehicleNum / 10 * 60),
                             rampLoop1MeanSpeed,
                             round(rampLoop1VehicleNum / 10 * 60),
                             rampLoop2MeanSpeed,
                             round(rampLoop2VehicleNum / 10 * 60),
                             rampLoop3MeanSpeed,
                             round(rampLoop3VehicleNum / 10 * 60), ','])
                             
        print("HW flow intensity: ", hw_vph * scale)
        print("Flow intensity 1: ", ramp1_vph)
        print("Flow intensity 2: ", ramp2_vph)
        print("Flow intensity 3: ", ramp3_vph)
        print("Program TL1: ", traci.trafficlight.getProgram(trafficLight1))
        print("Program TL2: ", traci.trafficlight.getProgram(trafficLight2))
        print("Program TL3: ", traci.trafficlight.getProgram(trafficLight3))
        
    if (step % 3600) == 0: # every 60 min....
        # Change highway flow intensity
        # 200-2000 veh/h
        # 10 equal length intervals
        scale = random.randint(1, 10)
        traci.simulation.setScale(scale)
        
        
    if (step % 1800) == 0: # every 30 min....
        # Change ramp flow intensity
        flow1 = random.randint(1, 10)
        # 40-400 veh/h
        # 10 equal interval
        ramp1_vph = 40 * flow1
            
        flow2 = random.randint(1, 10)
        # 40-400 veh/h
        # 10 equal interval
        ramp2_vph = 40 * flow2
            
        flow3 = random.randint(1, 10)
        # 40-400 veh/h
        # 10 equal interval
        ramp3_vph = 40 * flow3
        
    if (step % round(3600/ramp1_vph)) == 0: # defined vehicle per hour....
        car_id1 = ["car_ramp1_", car_num_ramp1]
        traci.vehicle.add(car_id1, "from_ramp1")
        car_num_ramp1 += 1
    if (step % round(3600/ramp2_vph)) == 0: # defined vehicle per hour....
        car_id2 = ["car_ramp2_", car_num_ramp2]
        traci.vehicle.add(car_id2, "from_ramp2")
        car_num_ramp2 += 1
    if (step % round(3600/ramp3_vph)) == 0: # defined vehicle per hour....
        car_id3 = ["car_ramp3_", car_num_ramp3]
        traci.vehicle.add(car_id3, "from_ramp3")
        car_num_ramp3 += 1
        
    step = step + 1

traci.close()

#changeTrafficLightProgram
#    while step < 36000:
#	#this runs one simulation step
#    traci.simulationStep()
#    if (step % 600) == 0: #every 10 min....
#        # Change traffic light program
#        tl1_prog += 1
#        if tl1_prog == 3:
#            tl1_prog = 0
#
#        traci.trafficlight.setProgram(trafficLight1, trafficLightProgs[0][tl1_prog])
#        if (step % 1800) != 0 and (step % 5400) != 0:
#            with open('output.csv', 'a', newline='') as csvfile:
#                writer = csv.writer(csvfile, delimiter=';',
#                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
#                writer.writerow([traci.trafficlight.getProgram(trafficLight1), traci.trafficlight.getProgram(trafficLight2), traci.trafficlight.getProgram(trafficLight3)])
#            print("Program TL1: ", traci.trafficlight.getProgram(trafficLight1))
#            print("Program TL2: ", traci.trafficlight.getProgram(trafficLight2))
#            print("Program TL3: ", traci.trafficlight.getProgram(trafficLight3))
#
#    if (step % 1800) == 0: #every 30 min....
#        # Change traffic light program
#        tl2_prog += 1
#        if tl2_prog == 3:
#            tl2_prog = 0
#        traci.trafficlight.setProgram(trafficLight2, trafficLightProgs[1][tl2_prog])
#        if (step % 5400) != 0:
#            with open('output.csv', 'a', newline='') as csvfile:
#                writer = csv.writer(csvfile, delimiter=';',
#                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
#                writer.writerow([traci.trafficlight.getProgram(trafficLight1), traci.trafficlight.getProgram(trafficLight2), traci.trafficlight.getProgram(trafficLight3)])
#            print("Program TL1: ", traci.trafficlight.getProgram(trafficLight1))
#            print("Program TL2: ", traci.trafficlight.getProgram(trafficLight2))
#            print("Program TL3: ", traci.trafficlight.getProgram(trafficLight3))
#
#    if (step % 5400) == 0: #every 90 min....
#        # Change traffic light program
#        tl3_prog += 1
#        if tl3_prog == 3:
#            tl3_prog = 0
#        traci.trafficlight.setProgram(trafficLight3, trafficLightProgs[2][tl3_prog])
#        with open('output.csv', 'a', newline='') as csvfile:
#            writer = csv.writer(csvfile, delimiter=';',
#                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
#            writer.writerow([traci.trafficlight.getProgram(trafficLight1), traci.trafficlight.getProgram(trafficLight2), traci.trafficlight.getProgram(trafficLight3)])
#        print("Program TL1: ", traci.trafficlight.getProgram(trafficLight1))
#        print("Program TL2: ", traci.trafficlight.getProgram(trafficLight2))
#        print("Program TL3: ", traci.trafficlight.getProgram(trafficLight3))
#    step = step + 1