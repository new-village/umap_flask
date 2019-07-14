# UMAP
Web Application Training

## Requirements
* Docker

## How to use

1. Set Parameters  
Rename environment file and Overwrite parameters
```bash:
$ cd <project_dir>
$ cp .env.sample .env
$ vim .env
```

2. Start Containers

```bash:
$ cd <project_dir>
$ docker-compose -f "docker-compose.yml" up -d --build
$ cd /umap
$ flask run
```

3. Start Application
```bash:
$ cd <project_dir>/umap
$ flask run
```

4. Access to http://localhost:5000/
