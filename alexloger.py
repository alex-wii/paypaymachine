import logging


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO,mode='a'):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file,mode=mode)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
logger = setup_logger('first_logger', 'first_logfile.log')
trainA_logger = setup_logger('TrainA_logger', 'TrainA_logger.log')
trainB_logger = setup_logger('TrainB_logger', 'TrainB_logger.log')
train_logger = setup_logger('TrainB_logger', 'train_logger.log')
order_logger = setup_logger('order_logger', 'order_logger.log')
do_order_logger = setup_logger('do_order_logger', 'do_order_logger.log')
station_logger = setup_logger('station_logger', 'station_logger.log',mode='a')