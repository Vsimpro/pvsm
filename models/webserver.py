import httpx

def is_webserver( host : str, port : int, timeout : int = 5 ):
    """
    Checks if a host & port is a webserver.
    
    Parameters:
        str : `host` the host
        int : `port` the port
        
    Returns:
        boolean: True if target is a webserver
    """
    
    try:
    
        _ = httpx.get(
            url     = f"http://{ host }:{ port }", 
            timeout = timeout
        )
        
        return True
    
    except httpx.RequestError:
        return False

