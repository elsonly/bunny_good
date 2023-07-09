# Docker Volume Backup

## Restore from backup
```
tar -C /tmp -xvf /c/docker_backup/backup-2023-07-09T08-19-00.tar.gz

docker run -d --name temp_restore_container -v mongo-data:/backup_restore alpine:3.18.2 sh -c 'while sleep 3600; do :; done'

docker cp /tmp/backup/mongodb temp_restore_container:/backup_restore
docker stop temp_restore_container
docker rm temp_restore_container

rm -R /tmp/backup
```