#Use to collect, visualise atomic structures
from ase.io import read

import numpy as np #Mathematical calculations

#Check length consistency of Bader files
def check_Bader_consistency(item, ini_q, fin_q):

    # Bader vs Bader
    if len(ini_q) != len(fin_q): #i.e., Check that Bader charge lengths are consistent
        raise ValueError( #If not, raise an error
            f"Atom count mismatch in {item['transition']}: "
            f"ini={len(ini_q)}, fin={len(fin_q)}"
        )

    #Atoms in each structure
    ini_atoms = read(item["ini_structure"])
    fin_atoms = read(item["fin_structure"])

    #Extract length of atoms
    ini_len = len(ini_atoms)
    fin_len = len(fin_atoms)

    # POSCAR vs Bader atom length
    if (fin_len != len(fin_q)) or (ini_len != len(ini_q)): #i.e., Check that Bader charge and POSCAR/CONTCAR lengths are consistent
        raise ValueError( #If not, raise an error
            f"Mismatch between POSCAR/CONTCAR and Bader atoms in {item['transition']}"
        )
    
    #Check element ordering consistency
    for i, (a_ini, a_fin) in enumerate(zip(ini_atoms, fin_atoms)):
        if a_ini.symbol != a_fin.symbol:
            raise ValueError(
                f"Element mismatch at index {i} in {item['transition']}: "
                f"{a_ini.symbol} (ini) != {a_fin.symbol} (fin)"
            )

#Check that Bader coordinates and POSCAR/CONTCAR coordinates are equivalent
def check_bader_alignment(atoms, acf_coords, tol=1e-3):

    #N.B. This tolerance is to not be confused with that of Bader charge difference.
    #This difference is to check that atoms in POSCAR/CONTCAR and ACF.dat are the same.
    #Here, difference should not be too large, and hence it is defaulted.

    pos = atoms.get_positions()  # Cartesian from ASE

    #Calculate difference based on absolute distance
    diff = np.linalg.norm(pos - acf_coords, axis=1)

    #Should be within threshold
    if np.max(diff) > tol:
        raise ValueError( #Else raise an error
            f"ACF.dat coordinates do not match POSCAR/CONTCAR "
            f"(max diff = {np.max(diff):.4f} Å)"
        )