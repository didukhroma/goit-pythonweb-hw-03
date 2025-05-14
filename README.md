# goit-pythonweb-hw-03

## How to start:

1. Create docker image

```
docker build . -t <your-image name>
```

2. Run docker container

```
docker run -itd -p 3000:3000 -v /storage/data.json <your-image name>
```
