import os
import subprocess
import xml.etree.ElementTree as ET
import pandas as pd

# Configuration
config_file = "region.sumocfg"
num_runs = 5
sumo_command = "sumo"  # ou "sumo-gui" si tu veux voir la simulation


emission_file = "emissions.xml"
pollution_file = "pollution_output.xml"
queue_file = "queue_detector_output.xml"

# Résultats accumulés
emissions_data = []
pollution_data = []
queue_data = []

def parse_emissions(file, run):
    tree = ET.parse(file)
    root = tree.getroot()
    for timestep in root.findall("timestep"):
        time = timestep.attrib["time"]
        for veh in timestep.findall("vehicle"):
            row = veh.attrib.copy()
            row["run"] = run
            row["time"] = time
            emissions_data.append(row)

def parse_pollution(file, run):
    tree = ET.parse(file)
    root = tree.getroot()
    for interval in root.findall("interval"):
        row = interval.attrib.copy()
        row["run"] = run
        pollution_data.append(row)

def parse_queue(file, run):
    tree = ET.parse(file)
    root = tree.getroot()
    for interval in root.findall("interval"):
        row = interval.attrib.copy()
        row["run"] = run
        queue_data.append(row)
#Lancer plusieurs simulations
for i in range(num_runs):
    print(f"🔁 Simulation {i+1}/{num_runs}...")
    subprocess.run([sumo_command, "-c", config_file], stdout=subprocess.DEVNULL)

    parse_emissions(emission_file, i + 1)
    parse_pollution(pollution_file, i + 1)
    parse_queue(queue_file, i + 1)

print("✅ Simulations terminées. Création du fichier Excel...")

# Convertir en DataFrames
df_emissions = pd.DataFrame(emissions_data)
df_pollution = pd.DataFrame(pollution_data)
df_queue = pd.DataFrame(queue_data)

# Sauvegarder dans Excel avec plusieurs feuilles
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df_emissions.to_excel(writer, sheet_name="Emissions", index=False)
    df_pollution.to_excel(writer, sheet_name="Pollution", index=False)
    df_queue.to_excel(writer, sheet_name="Queue", index=False)

print("📄 Données stockées dans 'output.xlsx'")
