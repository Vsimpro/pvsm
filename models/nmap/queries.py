# ================================== #
#              NMAP                  #
# ================================== #


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

