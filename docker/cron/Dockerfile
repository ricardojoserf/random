FROM i386/ubuntu:16.04
RUN apt-get update -y
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
# User ricardo
RUN useradd -ms /bin/bash ricardo
RUN echo 'ricardo:patata' | chpasswd
# User root
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
WORKDIR /app
EXPOSE 22
# Cron - source: https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
RUN apt-get -y install cron
COPY cron_job /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

CMD ["/usr/sbin/sshd", "-D"]

