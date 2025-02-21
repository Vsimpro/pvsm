import docker

# Initialize Docker client
client = docker.from_env()


def build_image( dockerfile_path : str, docker_image_name : str ) -> bool:
    """
    Builds the specified docker image, if it does not exist yet.

    Parameters:
        str : `dockerfile_path`, Path to the dockerfile for the image you want to build.
        str : `docker_image_name`, the tag/name of the dockerfile that's being built
    
    Returns:
        boolean: upon success.
    """
    
    print(f"[CONTAINERS] [+] Building a Docker image '{ docker_image_name }' from '{ dockerfile_path }' ...")
    
    # Ensure container isn't built already
    if image_exists( docker_image_name ):
        print(f"[CONTAINERS] [?] Image seems to exist .. Skipping building '{ docker_image_name }' ...")
        return True

    #
    #   Build the container
    #
    try:
        print( "debug:", dockerfile_path )
         
        client.images.build(
            path = dockerfile_path, 
            tag  = docker_image_name
        )
            
    except Exception as e:
        print(f"[CONTAINERS] [!!!] Error building image { docker_image_name }, exception str: {e}")
        return False
    
    print(f"[CONTAINERS] [+] Image '{ docker_image_name }' built successfully.")
    return True


def image_exists( image_name ) -> bool:
    """
    Check if image with a specified tag/name exists.

    Returns:
        boolean: upon success
    """

    try:
        
        # Image exists,
        client.images.get( image_name )
            
    # No such image,
    except docker.errors.ImageNotFound:
        return False
    
    # Generic exception catcher, treat as Image not existing,
    except Exception as e:
        print(f"[CONTAINERS] [!!!] Error checking image: {e}")
        return False
    
    return True


def run_container( image_name : str, command : str = "", image_path : str = "./", debug : bool = True ):
    """
    Start & run a specified container. In case it doesn't exist, try to build it.

    Parameters:
        str : `image_name` name of the docker container.
        str : `command` on entrypoint, what command you want to run. 
        str : `image_path` if container does not exist, try to build from this location.

    Returns
        str: the output of the container
    """

    output : str = ""

    #
    #   Ensure image exists, and if not, build it.
    #
    if not image_exists( image_name ):
        if not build_image( image_path, image_name ):
            print( "[CONTAINERS] [!] Unable to run the container." )
            return output
    
    #
    #   Run the container
    #
    try:
        container = client.containers.run(
            image_name,                
            command.split(),                  
            detach = True,                  
            auto_remove = True            
        )
        
        for log in container.logs( stream = True ):
            line = log.decode("utf-8").strip()
            output += line + "\n"
            
            
        #if debug: 
        print( "[CONTAINERS] Debug:", output )
    
    except Exception as e:
        print(f"[CONTAINERS] [!!!] Error running { image_name }: {e}")

    return output
