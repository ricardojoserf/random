#!/sh

#for i in $(docker ps -a | cut -d " " -f 1 | grep -v CON); do docker stop $i; docker rm $i; done
docker build -t bofapp .
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -d -p $1:22 --name test_sshd bofapp
#ssh-keygen -f "/root/.ssh/known_hosts" -R "[127.0.0.1]:33"
#ssh -l ricardo -p 33 127.0.0.1
