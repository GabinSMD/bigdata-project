from mrjob.job import MRJob
import datetime
from dateutil.relativedelta import relativedelta

class project_stock_history(MRJob):

  def configure_args(self):
    super(project_stock_history, self).configure_args()
    self.add_passthru_arg('--stockName', default='ACCIONA' ,help='Please introduce the name of the stock')

  def mapper(self, key, line):
    now = datetime.datetime.now()
    lastHour = now - datetime.timedelta(hours = 1)
    lastWeek = now - datetime.timedelta(weeks = 1)
    lastMonth = now - relativedelta(months=+1)

    data = line.split(',')

    name = data[0]
    maxSession = float(data[5])
    minSession = float(data[6])
    date = data[9]

    lineDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    if self.options.stockName.upper() == name:
      if lineDate > lastHour:
        yield(name,("lastHour",minSession,maxSession))
      if lineDate > lastWeek:
        yield(name,("lastWeek",minSession,maxSession))
      if lineDate > lastMonth:
        yield(name,("lastMonth",minSession,maxSession))

  def reducer(self, name, values):
    totalMonth=0
    totalWeek=0
    totalHour=0
    for last,minSession,maxSession in values:
      if last == "lastHour":
        if totalHour==0:
          minHour = minSession
          maxHour = maxSession
        if minSession < minHour:
          minHour=minSession
        if maxSession > maxHour:
          maxHour=maxSession
        totalHour+=1
      if last == "lastWeek":
        if totalWeek ==0:
          minWeek = minSession
          maxWeek = maxSession
        if minSession < minWeek:
          minWeek = minSession
        if maxSession > maxWeek:
          maxWeek = maxSession
        totalWeek+=1
      if last == "lastMonth":
        if totalMonth ==0:
          minMonth=minSession
          maxMonth=maxSession
        if minSession < minMonth:
          minMonth = minSession
        if maxSession > maxMonth:
          maxMonth = maxSession
        totalMonth+=1
    yield("Stock: "+name,("Minimal hour value: "+str(minHour),"Maximal hour value: "+str(maxHour),"Minmal week value: "+str(minWeek),"Maximal week value: "+str(maxWeek),"Minimal month value: "+str(minMonth),"Maximal month value: "+str(maxMonth)))

if __name__ == '__main__':
  project_stock_history.run()
