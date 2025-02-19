FROM alpine:latest

# Install necessary packages
RUN apk update && \
    apk add --no-cache \
    nmap 

# Set default command to Nmap
ENTRYPOINT ["nmap"]