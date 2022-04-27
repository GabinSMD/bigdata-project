from mrjob.job import MRJob
from datetime import datetime
import re

class project_top_date(MRJob):

  def configure_args(self):
    super(project_top_date, self).configure_args()
    self.add_passthru_arg('--searchDate', default='2022-04-22 18:00' ,help='Please introduce the date (format 2022-04-21 09:00)')

  def mapper(self, key, line):
    data= re.split('(\".*?\")', line)
    searchDate = datetime.strptime(self.options.searchDate, '%Y-%m-%d %H:%M')
    if(len(data)==7):
      nameTop5 = data[3]
      yield(1, ("top",nameTop5,str(searchDate)))
    else:
      data = line.split(',')
      name = data[0]
      lastQuote = float(data[1])
      date = data[9]
      lineDate = datetime.strptime(date, '%Y-%m-%d %H:%M')
      if lineDate == searchDate:
        yield(1, ("find",name, lastQuote))

  def reducer(self, name, values):
    topName=[]
    for tag, name, lastQuote in values:
      if tag == "top":
        try:
          topName.index(name)
        except ValueError:
          topName.append(name)
      if tag == "find":
        for i in topName:
          if name in i:
            yield("Stock: "+name,"Value: "+str(lastQuote))

if __name__ == '__main__':
  project_top_date.run()
