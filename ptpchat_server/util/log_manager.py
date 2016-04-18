import logging, pdb

class LogManager():

    logging_level = {
        "CRITICAL" : 50,
        "ERROR" : 40,
        "WARNING" : 30,
        "INFO" : 20,
        "DEBUG" : 10,
        "NOTSET" : 0
    }

    _format = "%(asctime)s - %(levelname)s - %(modulename)s - %(message)s"
    
    def __init__(self, log_name, file_name = None, module_name = "ptpchat-server", log_level="INFO"):
        if log_name is None or log_name is '':
            raise AttributeError("LogManager, must define a log name!")
            
        if log_level not in LogManager.logging_level:
            raise AttributeError("LogManager, must set an appropriate log level!")
    
        logging.basicConfig(filename=file_name, format=LogManager._format)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(LogManager.logging_level[log_level])
        self.extras = {'modulename' : module_name }

    def critical(self, message):
        self.logger.critical(message, extra=self.extras)
        
    def error(self, message):
        self.logger.error(message, extra=self.extras)
        
    def warning(self, message):
        self.logger.warning(message, extra=self.extras)
        
    def info(self, message):
        self.logger.info(message, extra=self.extras)
        
    def debug(self, message):
        self.logger.debug(message, extra=self.extras)