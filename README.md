# VTB Trends + RecSys + Search system

## Общая установка
Загрузить веса в папку `rec_engine/weights` из gdrive
```
https://drive.google.com/file/d/1JtzNXDsM2S6jd5A3PcnMT7UKPd_MrGf4/view?usp=sharing
https://drive.google.com/file/d/1H6hPRxKHWhBKvMfTsSsn4awT5KG7X3xo/view?usp=sharing
```

## Запуск системы
Запуск сервисов database, api, ui

`docker-compose --env-file .env up`


## Запуск скраперов + дамп в бд
```
cd scrapper/
bash build_docker.sh
bash run_docker_scrapping.sh
```

## Запуск разметки данных из бд

Тут вам, возможно, нужно в настройках докера увеличить кол-во памяти с 2гб.)
Подробнее: https://stackoverflow.com/questions/44417159/docker-process-killed-with-cryptic-killed-message

```
cd ../rec_engine
bash build_docker_tagging.sh
bash run_docker_tagging.sh
```




