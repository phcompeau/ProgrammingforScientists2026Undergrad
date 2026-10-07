#!/bin/bash
# Renders every automaton in the starter code to output/.
# Copy into python/src/cellular_automata and run from there (use python instead of python3 on Windows).
python3 main.py Moore rules/gol_rules.txt boards/gosper_gun.csv output/gosper_gun 20 400
python3 main.py vonNeumann rules/langton_loop.txt boards/langton_loop.csv output/langton_loop 20 900
python3 main.py Moore rules/gol_rules.txt boards/r_pentomino.csv output/r_pentomino 8 1200
python3 main.py Moore rules/gol_rules.txt boards/dinner_table.csv output/dinner_table 30 60
python3 main.py vonNeumann rules/rps.txt boards/rps_corners.csv output/rps_corners 5 500 color_maps/rps.txt
python3 main.py vonNeumann rules/rps.txt boards/rps_random.csv output/rps_random 5 300 color_maps/rps.txt
python3 main.py vonNeumann rules/rps.txt boards/rps_clusters.csv output/rps_clusters 5 180 color_maps/rps.txt
python3 main.py vonNeumann rules/rps_bounce.txt boards/rps_bounce.csv output/rps_bounce 15 200 color_maps/rps_bounce.txt
python3 main.py Moore rules/crystal_growth.txt boards/crystal_growth_1.csv output/crystal_growth_1 5 80 color_maps/crystal_growth.txt
python3 main.py Moore rules/crystal_growth.txt boards/crystal_growth_2.csv output/crystal_growth_2 5 60 color_maps/crystal_growth.txt
python3 main.py vonNeumann rules/bml_traffic.txt boards/bml_traffic_random.csv output/bml_traffic_random 5 400 color_maps/bml_traffic.txt
python3 main.py vonNeumann rules/bml_traffic.txt boards/bml_traffic_diagonal.csv output/bml_traffic_diagonal 5 400 color_maps/bml_traffic.txt
python3 main.py vonNeumann rules/bml_traffic.txt boards/bml_traffic_large.csv output/bml_traffic_large 3 300 color_maps/bml_traffic.txt
python3 main.py Moore rules/predator_prey.txt boards/predator_prey.csv output/predator_prey 5 270 color_maps/predator_prey.txt
python3 main.py Moore rules/predator_prey.txt boards/predator_prey_random.csv output/predator_prey_random 5 290 color_maps/predator_prey.txt
python3 main.py Moore rules/predator_prey.txt boards/predator_prey_clusters.csv output/predator_prey_clusters 5 540 color_maps/predator_prey.txt
python3 main.py vonNeumann rules/langtons_ant.txt boards/langtons_ant.csv output/langtons_ant 10 400 color_maps/langtons_ant.txt
python3 main.py Moore rules/wireworld.txt boards/wireworld.csv output/wireworld 5 110 color_maps/wireworld.txt
python3 main.py Moore rules/wireworld.txt boards/wireworld_pulse.csv output/wireworld_pulse 5 200 color_maps/wireworld.txt
python3 main.py Moore rules/wireworld.txt boards/wireworld_nae.csv output/wireworld_nae 10 50 color_maps/wireworld.txt
python3 main.py Moore rules/checkerboard.txt boards/checkerboard.csv output/checkerboard 5 20 color_maps/checkerboard.txt
