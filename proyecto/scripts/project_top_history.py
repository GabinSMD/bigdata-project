from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import re

class project_top_date(MRJob):
    def configure_args(self):
      super(project_top_date, self).configure_args()
      self.add_passthru_arg('--minDate', default='2022-04-16 09:30' ,help='Please introduce the first date (format: 2022-04-21 09:30)')
      self.add_passthru_arg('--maxDate', default='2022-04-26 19:40' ,help='Please introduce the last date (format: 2022-04-21 19:40)')


    def mapper(self, key, line):
        minDate = datetime.strptime(self.options.minDate, '%Y-%m-%d %H:%M')
        maxDate = datetime.strptime(self.options.maxDate, '%Y-%m-%d %H:%M')
        data=re.split('(\".*?\")',line)
        if len(data)==7:
            topName=data[3]
            yield(1,("top",topName,0,0,0))
        else:
            data=line.split(",")
            name = data[0]
            lastQuote = float(data[1])
            maxSession = float(data[5])
            minSession = float(data[6])
            date = data[9]
            lineDate = datetime.strptime(date, '%Y-%m-%d %H:%M')
            if lineDate >= minDate and lineDate <= maxDate:
              yield(1,("find",name,lastQuote,minSession,maxSession))

    def reducer(self, key, values):
        topName= []
        for tag, name, last, min, max in values:
            if tag== "top":
                try:
                  topName.index(name)
                except ValueError:
                  topName.append(name)
            if tag== "find":
                for i in topName:
                    if name in i:
                       yield(name,(last,min,max))

    def reducer2(self, name, values):
      total=0
      for last,min,max in values:
        if total==0:
          minTime=min
          maxTime=max
          initValue=last
        if min < minTime:
          minTime=min
        if max > maxTime:
          maxTime=max
        finalValue=last
        total+=1
      variation=round((((finalValue-initValue)/initValue)*100), 2)
      yield("Stock: "+name, ("Minimal value: "+str(minTime),"Maximal value: " +str(maxTime), "Variation: " + str(variation)+"%"))

    def steps(self):
     return [
         MRStep(mapper = self.mapper,
                reducer = self.reducer),
         MRStep(reducer = self.reducer2)
     ]

if __name__ == '__main__':
  project_top_date.run()
