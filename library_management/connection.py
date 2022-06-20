from sqlobject.mysql import builder


conn = builder()(user='root', password='josh@123', host='localhost', db='library')
