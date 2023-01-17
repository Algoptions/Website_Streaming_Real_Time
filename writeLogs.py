import datetime
import logging


class logsWrite:

    def __init__(self, fileName):
        if '*' in fileName:
            fileName = str(fileName).replace("*", "Z")
        self.fileName = "Management/real_time_data/logs/" + fileName + str(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + ".txt"

    def get_logger(self, name):
        log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            filename=self.fileName,
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(log_format))
        if len(logging.getLogger(name).handlers) == 0:
            logging.getLogger(name).addHandler(console)
        return logging.getLogger(name)
