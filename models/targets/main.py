import database.main as database


class Targets:
    create_targets_table = \
    """CREATE TABLE IF NOT EXISTS Targets (

        id   INTEGER   PRIMARY KEY AUTOINCREMENT,
        host TEXT      NOT NULL --

    );
    """

    insert_into_targets = """
        INSERT INTO Targets (
        
            host

        ) 
        VALUES (?);
    """

    get_target_by_host = """
        SELECT * FROM Targets WHERE host = ?;
    """

    get_targets = """
        SELECT * FROM Targets;
    """



def create_target_if_doesnt_exist( target : str ) -> int:
    """
    Check to see if the target already has been added to databse.
    If not, add it. In the end, return it's id in the table.
    
    Upon error, returns -1.
    
    Parameters:
        str : `target` the hostname or ip-address of the target.

    Returns:
        int : the Target.id of the hostname
    """
    target_id = -1
    
    try:
        
        # Try to find target from db
        result = database.query_database(
            Targets.get_target_by_host,
            (target,)
        )
        
        # Target exists, return ID.
        if result != []:
            target_id = int( result[ 0 ][ 0 ] )
            return target_id
            
        # Target doesn't exist, create a new one in db
        database.insert_data(
            Targets.insert_into_targets,
            (target,)
        )
        
        # Try to find target from db
        result = database.query_database(
            Targets.get_target_by_host,
            (target,)
        )
        
        target_id = int( result[ 0 ][ 0 ] )
        
    except Exception as e:
        print( f"[TARGETS] [!] Ran into an error while checking target ", target, " -- ", e )
    
    return target_id
        