"""
 * 
 *  Tool module for NMAP.
 *  One Nmap Object represents one scan, and it's results.
 *   
"""

import re, os, time

import containers.main as containers


MODULE_NAME = "NMAP"


class Nmap:
    
    #
    #   SQL Queries needed to handle NMAP & SQL
    #
    
    create_nmap_table = \
        """CREATE TABLE IF NOT EXISTS Nmap (

            id        INTEGER   PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,            --
            port      INTEGER   NOT NULL, --
            status    TEXT      NOT NULL, --
            service   TEXT      NOT NULL, --
            timestamp INTEGER   NOT NULL, --
            
            FOREIGN KEY( target_id ) REFERENCES Targets(id)

        );
    """


    insert_into_nmap = """
        INSERT INTO Nmap (
            target_id,
            port,
            status,
            service,  
            timestamp   
        ) 
        VALUES (?,?,?,?,?);
    """

    get_nmap_results_of_host = """
        SELECT host, port, status, service, timestamp 
        FROM Nmap 

        INNER JOIN Targets
        ON Nmap.target_id = Targets.id

        WHERE Targets.host = ?;
    """


    def __str__( self ):
        return f"[{MODULE_NAME} SCAN OBJECT] Timestamp: {self.timestamp}"
    
    def __init__( self, target_id : int, image_name : str = "nmap-module", image_path : str = "./models/nmap/Dockerfile"):
        self.logs      : str = ""
        self.target_id : int = target_id
        self.timestamp : int = time.time()
        
        self.image_name = image_name
        self.image_path = image_path
        
        # Ensure target has an ID.
        if target_id == -1:
            raise ValueError( "Target has an invalid id" )
        
        # Ensure dockerfile exists
        if not os.path.exists( self.image_path ):
            raise FileNotFoundError( "Dockerfile not in specified path: " + str(image_path) )
        
        
    def parse_ports( self ) -> list:
        """
        In essence, readies the logs for a SQL database.
        Reads the `self.logs` string and parses it into a list of tuples.

        Returns:
            list: of found ports on this scan
        """
    
        port_list   : list = []
        scan_output : str  = self.logs
        
        
        #
        #   Host is down, there is not listed ports in output.
        #
        if not (
                "PORT"    in scan_output and 
                "STATE"   in scan_output and 
                "SERVICE" in scan_output
            ): return port_list
        
        
        #
        #   Host is up
        #
        output_lines = scan_output\
            .split( "SERVICE\n" )[ 1 ]\
            .split("Nmap done:")[ 0 ]\
            .split( "\n" )
        
        for line in output_lines:

            output_line = re.split('\s+', line)
            if output_line == [""]:
                continue

            port    = output_line[ 0 ]
            status  = output_line[ 1 ]
            service = output_line[ 2 ]

            port_list.append( (self.target_id, port, status, service, self.timestamp) )
            
        return port_list


    def run( self, command : str ) -> bool:
        """
        Runs a NMAP scan with the command specified in parameters.  
        
        Uses a Docker container Wrapper. 
        See errors for guidance on setting up the needed Dockerfile & names
        
        Returns:
            boolean: status of success
        """
        global MODULE_NAME
        
        
        #
        #   Ensure needed parameters are present in obj
        #
        if (self.image_path == None or self.image_path == ""):
            raise ValueError( f"[{MODULE_NAME}] modules Docker image-path for Dockerfile can not be empty or 'None'!" )
        
        if (self.image_name == None or self.image_path == ""):
            raise ValueError( f"[{MODULE_NAME}] modules Docker image-name can not be empty or 'None'!" )
        
        
        self.logs += containers.run_container(
            image_name = self.image_name,
            image_path = self.image_path,
            command    = command,
            
            debug = False
        )
        
        
        return True