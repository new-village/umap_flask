# UMAP
UMAP is an all-in-one solution for Japanese horse racing prediction. It is possible to manage that are collecting data, creates models, applies model, view predictions and these functions automation on Web UI.

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
```

3. Start Application
```bash:
$ cd <project_dir>/umap
$ flask run
```

4. Access to http://localhost:5000/


## History
|    Date    | Version | Comment                                                                              |
|:----------:|:-------:|--------------------------------------------------------------------------------------|
| 2019/07/01 |   0.1   | Start Development Project.                                                           |


## Reference
#### Data Source
* [NetKeiba.com](http://db.netkeiba.com/) (Japanese Only)
* [SportsNavi](https://keiba.yahoo.co.jp/) (Japanese Only)

#### Development
* [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/)
* [Flask-PyMongo documentation](https://flask-pymongo.readthedocs.io/en/latest/)
