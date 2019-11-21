# Source: https://docs.docker.com/engine/examples/running_ssh_service/
FROM i386/ubuntu:16.04
RUN apt-get update -y
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN useradd -ms /bin/bash ricardo
# User ricardo
RUN echo 'ricardo:patata' | chpasswd
# User root
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
WORKDIR /app
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

