from datetime import datetime

class Logger:

  def info(self, service, method, msg):
    self.__write_log(service, method, msg, 30)

  def warn(self, service, method, msg):
    self.__write_log(service, method, msg, 40)

  def error(self, service, method, msg):
    self.__write_log(service, method, msg, 50)

  def __write_log(self, service, method, msg, level):
    with open('logs/{}.log'.format(service),'a+') as file:
        file.write('{}, {}, {}, {}, {}\n'.format(datetime.utcnow(), service, method, msg, level))