import logging
from utils.read_conf import ReadConf
from utils.db_connect import dbConnector as dbc
from ext_services.double_gis.presentor import insert_2gis_data

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Подгружаем конфигурационные файлы")
    ReadConf.read("ES", "ext_services_conf.ini")
    ReadConf.read("db", "db_conf.ini")

    logging.info("Подключаемся к БД")
    dbc.start_connect_db()

    logging.info("Берем данные из 2gis и кладем в базу")
    insert_2gis_data()

    logging.info('finish')
