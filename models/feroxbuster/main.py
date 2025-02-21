import time

import containers.main as containers


MODULE_NAME = "FEROXBUSTER"


class Feroxbuster:
    
    #
    #   SQL Queries needed to handle Feroxbuster & SQL
    #
    
    create_feroxbuster_table = \
    """CREATE TABLE IF NOT EXISTS Feroxbuster(
        
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        target_id     INTEGER   NOT NULL, --
        http_response TEXT      NOT NULL, --
        method        TEXT      NOT NULL, --
        lines         TEXT      NOT NULL, --
        words         TEXT      NOT NULL, --
        characters    TEXT      NOT NULL, --
        url           TEXT      NOT NULL, --
        timestamp     INTEGER   NOT NULL, --

        FOREIGN KEY (target_id) REFERENCES Targets(id)

    );
    """

    insert_into_feroxbuster = """
    INSERT INTO Feroxbuster (

        http_response,
        method,
        lines,
        words,
        characters,
        url,
        target_id,
        timestamp

    ) 
    VALUES (?,?,?,?,?,?,?,?);
    """

    get_feroxbuster_results_of_host = """
        SELECT *
        FROM   Feroxbuster
        INNER JOIN Targets
        ON Feroxbuster.target_id = Targets.id

        WHERE Targets.host = ?;
    """
    
    def __str__( self ):
        return f"[{MODULE_NAME} SCAN OBJECT] Timestamp: {self.timestamp}"
        
    def __init__( self, target_id : int, image_name : str = "feroxbuster-module", image_path : str = "./models/feroxbuster/"):
        self.logs      : str = ""
        self.target_id : int = target_id
        self.timestamp : int = time.time()
        
        self.image_name = image_name
        self.image_path = image_path
        
        
    # TODO: Redo this in a better manner
    def parse_results( self ) -> list:
        """
        In essence, readies the logs for a SQL database.
        Reads the `self.logs` string and parses it into a list of tuples.
        
        Returns:
            list : `port_list` list of tuples: (HTTP Response Code, HTTP Method, Lines, Words, Bytes, URL, Target_id, Timestamp)
        """

        results         : str   = self.logs
        timestamp       : float = time.time()
        normalized_data : list  = []

        if "skipping..." in results:
            return []
        
        for line in results.split("\n"):

            # Skip first line
            if "Auto-filtering".lower() in line.lower():
                continue

            # Skip last line
            if "Scanning:".lower() in line.lower():
                continue


            # 0: HTTP Response code
            # 1: HTTP Method
            # 2: Lines
            # 3: Words 
            # 4: Characters / bytes
            # 5: URL    
            normalized_line = list()
            if line == "":
                continue
                
            if "=>" in line:
                line = line.split("=>")[0]
                
            for result in line.split(" "):
                
                if result == "":
                    continue
                
                if result in normalized_line:
                    continue
                
                normalized_line.append( result.strip() )

            normalized_line.append( self.target_id )
            normalized_line.append( timestamp )
            normalized_data.append( normalized_line )
            
        return  normalized_data
    
    
    def run( self, command : str ) -> bool:
        """
        Runs a NMAP scan with the command specified in parameters.  
        
        Uses a Docker container Wrapper. 
        See errors for guidance on setting up the needed Dockerfile & names
        
        Returns:
            boolean: status of success
        """
        global MODULE_NAME

        # Tweak the command        
        command += " --quiet --rate-limit=50"
        if ":443" not in command:
            command += " --insecure"
        
        #
        #   Ensure needed parameters are present in obj
        #
        if (self.image_path == None or self.image_path == ""):
            raise ValueError( f"[{MODULE_NAME}] modules Docker image-path for Dockerfile can not be empty or 'None'!" )
        
        if (self.image_name == None or self.image_path == ""):
            raise ValueError( f"[{MODULE_NAME}] modules Docker image-name can not be empty or 'None'!" )
        
        
        print( f"[{ MODULE_NAME}] Beginning a scan with command: feroxbuster --url", command, "\n\n" )
        self.logs += containers.run_container(
            image_name = self.image_name,
            image_path = self.image_path,
            command    = command,
            
            debug = False
        )
        
        return True
