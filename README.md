# VTB Trends + RecSys + Search system

## Запуск системы
Запуск сервисов database, api, ui
'docker-compose --env-file .env up'

'''
cd scrapper/
bash build_docker.sh
'''

## Запуск скраперов + дамп в бд
bash run_docker_scrapping.sh

cd ../rec_engine

Загрузить веса в папку 'weights' из gdrive
https://drive.google.com/file/d/1JtzNXDsM2S6jd5A3PcnMT7UKPd_MrGf4/view?usp=sharing
https://drive.google.com/file/d/1H6hPRxKHWhBKvMfTsSsn4awT5KG7X3xo/view?usp=sharing

'bash build_docker.sh'

Тут вам, возможно, нужно в настройках докера увеличить кол-во памяти с 2гб.)
Подробнее: https://stackoverflow.com/questions/44417159/docker-process-killed-with-cryptic-killed-message

Запуск разметки данных из бд
'bash run_docker_tagging.sh'

