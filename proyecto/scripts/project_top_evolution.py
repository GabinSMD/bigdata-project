from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import math

class project_top_evolution(MRJob):

  def configure_args(self):
    super(project_top_evolution, self).configure_args()
    self.add_passthru_arg('--pourcentage', default='-11' ,help='Please introduce the pourcentage search')
    self.add_passthru_arg('--minDate', default='2022-04-16 09:30' ,help='Please introduce the first date (format: 2022-04-21 09:30)')
    self.add_passthru_arg('--maxDate', default='2022-04-26 19:40' ,help='Please introduce the last date (format: 2022-04-21 19:40)')

  def mapper(self, key, line):
    minDate = datetime.strptime(self.options.minDate, '%Y-%m-%d %H:%M')
    maxDate = datetime.strptime(self.options.maxDate, '%Y-%m-%d %H:%M')
    data=re.split('(\".*?\")',line)
    if len(data)==7:
        topName=data[3]
        yield("top",(topName,math.floor(float(self.options.pourcentage))))
    else:
        data = line.split(',')
        name = data[0]
        lastQuote = float(data[1])
        date = data[9]

        minDate = datetime.strptime(self.options.minDate, '%Y-%m-%d %H:%M')
        maxDate = datetime.strptime(self.options.maxDate, '%Y-%m-%d %H:%M')
        lineDate = datetime.strptime(date, '%Y-%m-%d %H:%M')
        if lineDate >= minDate and lineDate <= maxDate:
            yield(name,(name,lastQuote))

  def reducer(self, tag, values):
    if tag == "top":
      for name, value in values:
        yield(1, (name, value))
    else:
      total=0
      for name, value in values:
        if total==0:
          initValue=value
        finalValue=value
        total+=1
      pourcent=round(((finalValue-initValue)/initValue)*100,2)
      yield(2,(name, pourcent))

  global topName
  global pourc
  topName=[]
  pourc=0
  def reducer2(self, tag, values):
    global pourc
    if tag == 1:
      for name, value in values:
          try:
            topName.index(name)
          except ValueError:
            topName.append(name)
          pourc=value
    if tag == 2:
      for name, value in values:
         if math.floor(value) == pourc:
            for i in topName:
               if name in i:
                 yield("Stock: "+name,"Variation: "+str(value)+"%")


  def steps(self):
      return [
          MRStep(mapper = self.mapper,
                 reducer = self.reducer),
          MRStep(reducer = self.reducer2)
      ]

if __name__ == '__main__':
  project_top_evolution.run()
