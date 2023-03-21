# Dockerfile

## Shell

```dockerfile
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND noninteractive
```

## Install apt dependencies

Install listed:
```dockerfile
RUN apt-get update --fix-missing                                \
    && apt-get install -y --no-install-recommends [p1,p2,...]   \
    && apt-get clean                                            \
    && apt-get autoremove -y                                    \
    && rm -rf /var/lib/apt/lists/*
```

Install from file (each package in a new line):
```dockerfile
COPY resources/system_requirements.txt /resources/system_requirements.txt
RUN apt-get update --fix-missing                                                                \
    && xargs apt-get install -y --no-install-recommends < /resources/system_requirements.txt    \
    && apt-get clean                                                                            \
    && apt-get autoremove -y                                                                    \
    && rm -rf /var/lib/apt/lists/*
```

## SSH server

Requirements: `openssh-server`

Configure:
```dockerfile
RUN mkdir /var/run/sshd                                                                                     \
    && sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config                \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd   \
    && echo "export VISIBLE=now" >> /etc/profile
ENV NOTVISIBLE "in users profile"
```

Expose:
```dockerfile
EXPOSE 22
```

Entrypoint:
```dockerfile
ENTRYPOINT ["/usr/sbin/sshd", "-D"]
```

sshd.sv.conf (only for supervisord)
```
[program:sshd]
command=/usr/sbin/sshd -D
```

## Users (required for secure ssh since root ssh is set to be prohibited)

```dockerfile
# Change the initial root password
# !!!IMPORTANT: PASSWORD MUST BE CHANGED IMMIDIATELY AFTER FIRST LOGIN!!!
RUN echo 'root:nehezjelszo' | chpasswd

# Create user to use at SSH connection
# !!!IMPORTANT: PASSWORD MUST BE CHANGED IMMIDIATELY AFTER FIRST LOGIN!!!
ARG USERNAME=ssh-user
ARG GROUPNAME=ssh-group
RUN groupadd ${GROUPNAME}                                                 \
    && useradd -s /bin/bash -g ${GROUPNAME} [-G g1,g2,g3] -m ${USERNAME}  \
    && echo "${USERNAME}:nehezjelszo" | chpasswd                          \
    && mkdir /home/${USERNAME}/.ssh                                       \
    && chown -R ${USERNAME}:${GROUPNAME} /home/${USERNAME}/
```

## Supervisord

Requirements: `supervisor`

Configure:
```dockerfile
# Copy supervisord base configuration
COPY resources/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy each program config after installing them
COPY resources/p1.sv.conf /etc/supervisor/conf.d/p1.sv.conf
COPY resources/p2.sv.conf /etc/supervisor/conf.d/p2.sv.conf
```

Entrypoint:
```dockerfile
ENTRYPOINT ["/usr/bin/supervisord"]
```

supervisord.conf
```
[supervisord]
nodaemon=true

[include]
files = /etc/supervisor/conf.d/*.conf
```