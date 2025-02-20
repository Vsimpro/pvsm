"""
 *  Tech Demo:
 *  Programmatic Vulnerability Scanning & Management 
 *
 * -Vs1m, 19/02/2025
"""
import sys
import database.main as database

# importing of tooling modules
from models.nmap.main import Nmap

from models.targets.main import Targets
import models.targets.main as targets 


#
#   Main Loop of the program
#
def main( target : str ):
    #
    #   Prepare database
    #
    tables = {
        "Nmap"     : Nmap.create_nmap_table,
        "Targets"  : Targets.create_targets_table
    }
    
    database.initialize_db()
    database.create_tables(
        tables
    )
    
    
    #
    #   Run the scan
    #
    
    # Ensure target has been added to db
    target_id = targets.create_target_if_doesnt_exist( target )
    
    # Prepare the can object & run the can
    port_scan = Nmap( target_id )
    port_scan.run( f"{target}" )

    # Parse results
    ports = port_scan.parse_ports()
    
    # Store results
    database.insert_data(
        Nmap.insert_into_nmap,
        ports
    )
    
    #
    #   Check results
    #
    result = database.query_database(
        Nmap.get_nmap_results_of_host,
        (target,)
    )

    print( result )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[MAIN] Incorrect amount of arguments. Usage: python3 main.py <TARGET>")
        exit()
    
    main( str(sys.argv[1]) )
