import os #Operating system
from geometry import build_shift, apply_shift #Atomic shifting functions
from plotting import view_cleanup #Create a temporary figure(s)
import json #JS file
import numpy as np #Mathematical calculations

_current_mode = None #Global variable in selecting mode of imaging

#Obtain integers for certain prompts. If not an integer, then repeat.
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer (e.g., -1, 0, 1).")

#Choose whether to apply shifts to all or some images
def choose_mode():

    global _current_mode #Global variable
    if _current_mode is not None:
        return _current_mode

    #Choose a figure collection method
    while True:
        print("\nSelect shift mode:")
        print("1: Same shift per (ini, fin) pair") #Mode 1: same shift for each (ini, fin) image pair
        print("2: Manual shift for EACH structure") #Mode 2: manual shift for each individual image
        print("3: Same shift for ALL images") #Mode 3: same shift for each individual image

        #Which method? Select an integer among 1, 2, and 3.
        mode = get_int("Enter mode (1/2/3): ")
        #Ask if correct, else restart loop
        if mode in [1, 2, 3]:
            confirm_mode = input(f"Confirm mode {mode}? (y/n): ").lower() #Confirmation
            if confirm_mode == "y":
                _current_mode = mode #Keep selected method constant throughout program
                return mode

        print("Invalid mode, try again.\n")

#Used to accept a result
def confirm():
    while True:
        ans = input("Accept this result? (y/n): ").lower()
        if ans in ["y", "n"]:
            return ans == "y"
        print("Please enter 'y' or 'n'.")

#If Mode 3, save the constant shift in a json file to reuse it
def save_shift(shift, filename="shift.json"):
    data = {
        "shift": shift.tolist()
    }
    with open(filename, "w") as f:
        json.dump(data, f)
#If Mode 3, load the constant shift from the saved json file to reuse it
def load_shift(filename="shift.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f) #Open is possible
        return np.array(data["shift"])
    except FileNotFoundError:
        return None
#If Mode 3, delete the saved json shift file after each file is looped through
def delete_shift(filename="shift.json"):
    try:
        os.remove(filename) #Delete if possible
    except FileNotFoundError:
        pass

#Dependin on the mode selected, apply appropriate imaging collection method
def process_structures(atoms_ini, atoms_fin):

    mode = choose_mode() #Which mode?

    if mode == 1: #Mode 1: same shift for each (ini, fin) image pair

        while True:
            shift = build_shift(atoms_ini,get_int) #Prepare shift
            test_ini = apply_shift(atoms_ini, shift) #Apply shift to initial image
            test_fin = apply_shift(atoms_fin, shift) #Apply shift to initial image

            view_cleanup(test_fin) #Check images temporarily if they look OK, especially after input shift constant factor

            if confirm(): #Accept result or not
                break

        return test_ini, test_fin #Return shifted results

    elif mode == 2: #Mode 2: manual shift for each individual image

        results = [] #Initialise
        for i in [atoms_ini, atoms_fin]: #Loop through each dataset
            while True:
                shift = build_shift(i,get_int) #Prepare shift
                test = apply_shift(i,shift) #Apply shift to initial/final image
                view_cleanup(test) #Check images temporarily if they look OK, especially after input shift constant factor

                if confirm(): #Accept result or not
                    results.append(test) #Collect data
                    break

        test_ini = results[0] #Same output variables as other modes
        test_fin = results[1]

        return test_ini, test_fin #Return shifted results

    elif mode == 3: #Mode 3: same shift for each individual image

        shift = load_shift() #Load constant shift

        if shift is None: #If no shift file, save one first and then reuse it

            while True:
                shift = build_shift(atoms_ini,get_int) #Prepare shift
                test_ini = apply_shift(atoms_ini,shift) #Apply shift to initial image
                test_fin = apply_shift(atoms_fin,shift) #Apply shift to final image

                view_cleanup(test_fin) #Check images temporarily if they look OK, especially after input shift constant factor

                if confirm(): #Accept result or not
                    save_shift(shift) #Save shift json file
                    break

        else:
            test_ini = apply_shift(atoms_ini, shift) #Same output variables as other modes
            test_fin = apply_shift(atoms_fin, shift)

        return test_ini, test_fin #Return shifted results
