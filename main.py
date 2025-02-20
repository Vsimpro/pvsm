"""
 *  Tech Demo:
 *  Programmatic Vulnerability Scanning & Management 
 *
 * -Vs1m, 02/2025
"""
import sys
import database.main as database

# importing of tooling modules
import models.webserver as webservers
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
    #port_scan.run( f"{target}" )

    # Parse results
    #ports = port_scan.parse_ports()
    
    # Store results
    #database.insert_data(
    #    Nmap.insert_into_nmap,
    #    ports
    #)
    
    #
    #   Check results
    #
    results = database.query_database(
        Nmap.get_nmap_results_of_host,
        (target,)
    )

    for result in results:
        port = result[ 1 ].split("/")[ 0 ]
        
        port_has_webserver = webservers.is_webserver( target, port )
        if port_has_webserver:
            print( f"[MAIN] Port { port } of target { target } suspected to be a webserver." )
            pass
        
        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[MAIN] Incorrect amount of arguments. Usage: python3 main.py <TARGET>")
        exit()
    
    main( str(sys.argv[1]) )
