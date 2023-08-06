import os
import json
import logging


class myconfig:
    def __init__(self, attributes):
        for k, v in attributes.items():
            setattr(self, k, v)

class mylogger :

    def info(self,msg_str):
        logging.info(msg_str)
    def debug(self,msg_str):
        logging.debug(msg_str)
    def warning(self,msg_str):
        logging.warning(msg_str)
    def error(self,msg_str):
        logging.error(msg_str)


class myapi:

    def __init__(self):
        with open(os.path.join(os.getcwd(),'operator.json')) as json_file:
            config_data = json.load(json_file)['config']
        del config_data['$type']
        self.config = myconfig(config_data)
        self.logger = mylogger()

    class Message:
        def __init__(self, body=None, attributes=""):
            self.body = body
            self.attributes = attributes

    def send(self,port,msg):
        if isinstance(msg,str) :
            print('PORT {}: {}'.format(port,msg))
        else :
            print('PORT {}: \nattributes: {}\nbody: {}'.format(port,str(msg.attributes),str(msg.body)))

    def add_generator(self,func):
        func()


try:
    api
except NameError:
    api = myapi()
