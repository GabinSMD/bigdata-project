from mrjob.job import MRJob
from datetime import datetime
import math

class project_stock_evolution(MRJob):

  def configure_args(self):
    super(project_stock_evolution, self).configure_args()
    self.add_passthru_arg('--pourcentage', default='1' ,help='Please introduce the pourcentage search')
    self.add_passthru_arg('--minDate', default='2022-04-16 09:30' ,help='Please introduce the first date (format 2022-04-21 09:30)')
    self.add_passthru_arg('--maxDate', default='2022-04-22 19:40' ,help='Please introduce the last date (format 2022-04-21 19:40)')

  def mapper(self, key, line):

    data = line.split(',')

    name = data[0]
    lastQuote = float(data[1])
    date = data[9]

    minDate = datetime.strptime(self.options.minDate, '%Y-%m-%d %H:%M')
    maxDate = datetime.strptime(self.options.maxDate, '%Y-%m-%d %H:%M')
    lineDate = datetime.strptime(date, '%Y-%m-%d %H:%M')

    if lineDate >= minDate and lineDate <= maxDate:
      yield(name,(lastQuote,math.floor(float(self.options.pourcentage))))

  def reducer(self, name, values):
    total=0
    finalValue=0
    initValue=0
    for lastQuote, pourcentage in values:
      if total==0:
        initValue=lastQuote
      finalValue=lastQuote
      total+=1
    pourcent=round(((finalValue-initValue)/initValue)*100,2)
    if math.floor(pourcent) == pourcentage:
      yield("Stock: "+name,("Initial value: "+str(initValue), "Final value: "+str(finalValue), "Variation: " +str(pourcent)+"%"))

if __name__ == '__main__':
  project_stock_evolution.run()
