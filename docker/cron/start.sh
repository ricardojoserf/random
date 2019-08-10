#!/sh
for i in $(docker ps -a | cut -d " " -f 1 | grep -v CON); do docker stop $i; docker rm $i; done
docker build -t bofapp .
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -d -p $1:22 --name test_sshd bofapp
docker exec $(docker ps -a | grep -v CON | cut -d " " -f 1) cron
