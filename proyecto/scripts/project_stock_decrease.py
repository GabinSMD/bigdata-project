from mrjob.job import MRJob
from mrjob.step import MRStep
from dateutil.relativedelta import relativedelta

import datetime

class project_stock_decrease(MRJob):

  def mapper(self, key, line):

    now = datetime.datetime.now()

    data = line.split(',')

    name = data[0]
    lastQuote = float(data[1])
    date = data[9]

    lastWeek = now - datetime.timedelta(weeks = 1)
    lastMonth = now - relativedelta(months=+1)

    lineDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')

    if lineDate > lastWeek:
      yield(name,("lastWeek",lastQuote))
    if lineDate > lastMonth:
      yield(name,("lastMonth",lastQuote))

  def reducer(self, name, values):
    totalWeek=0
    totalMonth=0
    monthFinalValue=0
    weekFinalValue=0
    monthInitValue=0
    weekInitValue=0
    weekDiff=0
    monthDiff=0
    for last,lastQuote in values:
      if last == "lastWeek":
        if totalWeek==0:
          weekInitValue=lastQuote
        weekFinalValue=lastQuote
        weekDiff=round(((weekFinalValue-weekInitValue)/weekInitValue)*100, 2)
        totalWeek+=1
      if last == "lastMonth":
        if totalMonth==0:
          monthInitValue=lastQuote
        monthFinalValue=lastQuote
        monthDiff=round(((monthFinalValue-monthInitValue)/monthInitValue)*100, 2)
        totalMonth+=1
    yield(1,(name,weekDiff,monthDiff))

  def reducer2(self, key, values):
    #Month
    monthListName = []
    monthListValue = []
    #Week
    weekListName = []
    weekListValue = []
    for name, week, month in values:
      weekListValue.append(week)
      weekListName.append(name)
    #Month
      monthListValue.append(month)
      monthListName.append(name)
    #Week
    for index in range (1, len(weekListValue)):
      week_current_value = weekListValue[index]
      week_current_name = weekListName[index]
      week_current_left_index = index-1
      while week_current_left_index >= 0 and weekListValue[week_current_left_index] > week_current_value:
        weekListValue[week_current_left_index+1] = weekListValue[week_current_left_index]
        weekListName[week_current_left_index+1] = weekListName[week_current_left_index]
        week_current_left_index -= 1
        weekListValue[week_current_left_index+1] = week_current_value
        weekListName[week_current_left_index+1] = week_current_name
    #Month
    for index in range (1, len(monthListValue)):
      month_current_value = monthListValue[index]
      month_current_name = monthListName[index]
      month_current_left_index = index-1
      while month_current_left_index >= 0 and monthListValue[month_current_left_index] > month_current_value:
        monthListValue[month_current_left_index+1] = monthListValue[month_current_left_index]
        monthListName[month_current_left_index+1] = monthListName[month_current_left_index]
        month_current_left_index -= 1
        monthListValue[month_current_left_index+1] = month_current_value
        monthListName[month_current_left_index+1] = month_current_name
    #Week
    weekListMerge=zip(weekListName,weekListValue)
    i=0
    #Month
    monthListMerge=zip(monthListName,monthListValue)
    y=0
    #Week
    for currentName,weekValue in weekListMerge:
      i+=1
      if i > 0 and i <= 5:
        yield("Rank of the last week: "+str(i),("Stock: "+currentName,"Decrease of: "+str(weekValue)+"%"))
    #Month
    for currentName,monthValue in monthListMerge:
      y+=1
      if y > 0 and y <= 5:
        yield("Rank of the last month: "+str(y),("Stock: "+currentName,"Decrease of: "+str(monthValue)+"%"))

  def steps(self):
      return [
          MRStep(mapper = self.mapper,
                 reducer = self.reducer),
          MRStep(reducer = self.reducer2)
      ]

if __name__ == '__main__':
  project_stock_decrease.run()
