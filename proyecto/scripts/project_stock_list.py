from mrjob.job import MRJob
from mrjob.step import MRStep

class project_stock_list(MRJob):

  def mapper(self, key, line):

    data = line.split(',')
    name = data[0]
    lastQuote = float(data[1])
    maxSession = float(data[5])
    minSession = float(data[6])
    yield(name,(minSession,maxSession,lastQuote))

  def reducer(self, name, values):
    total=0
    for minSession,maxSession,lastQuote in values:
      if total==0:
        minLocal=minSession
        maxLocal=maxSession
        initValue=lastQuote
      if minSession < minLocal:
        minLocal = minSession
      if maxSession > maxLocal:
        maxLocal = maxSession
      finalValue=lastQuote
      total+=1
    yield("Stock: "+name,("Minimum value: "+str(minLocal),"Maximum value: "+str(maxLocal), "Initial value: "+str(initValue), "Final value: "+ str(finalValue)))

if __name__ == '__main__':
  project_stock_list.run()
