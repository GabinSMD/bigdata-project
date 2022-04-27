from mrjob.job import MRJob
from datetime import datetime

class project_stock_infos(MRJob):

  def configure_args(self):
    super(project_stock_infos, self).configure_args()
    self.add_passthru_arg('--stockName', default='ACCIONA' ,help='Please introduce the name of the stock')
    self.add_passthru_arg('--minDate', default='2022-04-21 09:30' ,help='Please introduce the first date (forma: 2022-04-21 09:30)')
    self.add_passthru_arg('--maxDate', default='2022-04-21 19:40' ,help='Please introduce the last date (format: 2022-04-21 19:40)')

  def mapper(self, key, line):

    data = line.split(',')

    name = data[0]
    lastQuote = float(data[1])
    maxSession = float(data[5])
    minSession = float(data[6])
    date = data[9]

    minDate = datetime.strptime(self.options.minDate, '%Y-%m-%d %H:%M')
    maxDate = datetime.strptime(self.options.maxDate, '%Y-%m-%d %H:%M')
    lineDate = datetime.strptime(date, '%Y-%m-%d %H:%M')

    if self.options.stockName.upper() == name:
      if lineDate > minDate and lineDate < maxDate:
        yield(name,(lastQuote,minSession,maxSession))

  def reducer(self, name, values):
    total=0
    for lastQuote,minSession,maxSession in values:
      if total==0:
        maxLocal=maxSession
        minLocal=minSession
        initValue=lastQuote
      if maxSession>maxLocal:
        maxLocal=maxSession
      if minSession<minLocal:
        minLocal=minSession
      total+=1
    increase = round(((maxLocal-initValue)/initValue)*100,2)
    decrease = round(((minLocal-initValue)/initValue)*100,2)
    yield("Stock: "+name,("Minimum value: "+str(minSession),"Maximum value: "+str(maxSession),"Increase between initial and maximum value: "+str(increase)+"%","Decrease between initial and minimal value: "+str(decrease)+"%"))

if __name__ == '__main__':
  project_stock_infos.run()
