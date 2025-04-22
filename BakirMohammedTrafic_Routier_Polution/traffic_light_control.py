import traci
import sumolib
import time

# Chemin vers ton fichier .sumocfg
SUMO_BINARY = "sumo-gui"  
CONFIG_FILE = "region.sumocfg"

# Lancer SUMO via TraCI
traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

# ID du feu à contrôler (vérifie dans le fichier .net.xml si c'est bien "n2")
traffic_light_id = "n2"
detector_id = "queue_detector_edge1"

# Boucle de simulation
step = 0
while step < 1000:
    traci.simulationStep()

    # Lire la file d'attente
    queue_length = traci.lanearea.getLastStepHaltingNumber(detector_id)
    print(f"Step {step} - Halting vehicles: {queue_length}")

    # Si plus de 10 véhicules en attente, passer le feu au vert (phase 0)
    if queue_length > 10:
        traci.trafficlight.setPhase(traffic_light_id, 1)

    step += 1
    time.sleep(0.1) 


traci.close()
