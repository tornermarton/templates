# Docker Compose

Connect to local bound port with ssh forwarding: 
`ssh user@1.2.3.4 [-f] -N -L [REMOTE]:localhost:[HOST]`. If -f is provided the 
process is started in the background and must be killed manually. To find the 
running processes: `ps -lef | grep ssh`. Use `kill [ID]` to kill the connection.

```yaml
version: "3.6"

services:
  master:
    image: example/image:tag
    container_name: example-container
    hostname: example-container
    user: user:group
    command: override command
    ports:
      - "[HOST]:[CONTAINER]"
      - "127.0.0.1:[HOST]:[CONTAINER]" # only local, is not exposed to outside net
    env_file:
      - .env
    environment:
      - EXAMPLE_ENV_VARIABLE=value
    volumes:
      - example-volume:/path/in/container
      - /path/on/host:/path/in/container
    tty: true
    depends_on:
      - dependency-container
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"

volumes:
  example-volume:

networks:
  default:
    name: example
```
