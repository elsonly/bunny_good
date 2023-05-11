# prefect

## install
```
install.bat
```

## deploy-server

start server
```
server.bat
```

## configure
after start the server, configure the worker

```
conda activate prefect-env
prefect work-pool create --type process local-work
cd ./cmoney
prefect deploy --all
```

## deploy-worker

start worker
```
worker.bat
```