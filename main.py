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

from models.nmap.main        import Nmap
from models.feroxbuster.main import Feroxbuster

import models.targets.main as targets 
from models.targets.main import Targets




#
#   Main Loop of the program
#
def main( target : str ):
    #
    #   Prepare database
    #
    tables = {
        "Nmap"        : Nmap.create_nmap_table,
        "Targets"     : Targets.create_targets_table,
        "Feroxbuster" : Feroxbuster.create_feroxbuster_table
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
    
    # Store results
    database.insert_data(
        Nmap.insert_into_nmap,
        port_scan.parse_ports()
    )
    
    #
    #   Check results
    #
    results = database.query_database(
        Nmap.get_latest_nmap_results_of_host,
        (target,)
    )

    #
    #   Parse results & Start Feroxbuster scan on webservers.
    #
    content_enum_scan_targets = []
    for result in results:
        port = result[ 1 ]
        
        port_has_webserver = webservers.is_webserver( target, port )
        if not port_has_webserver:
            continue    
            
        print( f"[MAIN] Port { port } of target { target } suspected to be a webserver." )
        content_enum_scan_targets.append( f"{target}:{port}" )
        
        
    for scan_target in content_enum_scan_targets:
        # start feroxbuster
        content_enum = Feroxbuster( target_id )
        content_enum.run( f"http://{scan_target}" ) 
        
        # Store results
        database.insert_data(
            Feroxbuster.insert_into_feroxbuster,
            content_enum.parse_results()
        )

        
    #
    #   Check results
    #
    for scan_target in content_enum_scan_targets:
        results = database.query_database(
            Feroxbuster.get_latest_feroxbuster_results_of_host,
            (scan_target,)
        )

        print(f"\n[MAIN] Listing content enum results of {scan_target}:")
        for result in results:
            status, endpoint, target = result[ 3 ], result[ 8 ], result[ 1 ]
            print( f"[MAIN] Target: {target} Endpoint: { endpoint }, with status { status }" )



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("[MAIN] Incorrect amount of arguments. Usage: python3 main.py <TARGET>")
        exit()
    
    main( str(sys.argv[1]) )
