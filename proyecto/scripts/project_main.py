from datetime import datetime
import os

now = datetime.now()
nowMinute = now.minute
nowHour = now.hour
nowMonth = now.month
nowYear = now.year
nowDay = now.day
nowWeek = datetime.today().isocalendar()[1]

fileHourly = 'hourlyResult_'+str(nowYear)+'-'+str(nowMonth)+'-'+str(nowDay)+'-'+str(nowHour)+'h'
fileDaily = 'dailyResult_'+str(nowYear)+'-'+str(nowMonth)+'-'+str(nowDay)
fileMonthly = 'monthlyResult_'+str(nowYear)+'-'+str(nowMonth)
fileWeekly = 'weeklyResult_'+str(nowYear)+'-W'+str(nowWeek)
pathFileHourly = '/home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay)+'/'+fileHourly

os.makedirs('/home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay), exist_ok = True)
os.system('python /home/alumno/bigdatapracticas/proyecto/scripts/scraper.py > '+ pathFileHourly)

with open (pathFileHourly,'r') as currentFile:
  overwrite=[]
  for index,line in enumerate(currentFile):
    newLine=""
    data = line.strip().split(',')
    if "/" in data[9]:
      date = datetime.strptime(data[9], "%d/%m")
      date = datetime(date.today().year, date.month, date.day)
    elif ":" in data[9]:
      date = datetime.strptime(data[9], "%H:%M")
      date = now.replace(hour=date.hour, minute=date.minute, second=0, microsecond=0)
    data[9]=str(date.strftime("%Y-%m-%d %H:%M"))
    for i in range(len(data)):
      if i == 0:
        newLine = data[i]
      else:
        newLine = newLine+','+data[i]
    newLine = newLine+'\n'
    overwrite.append(newLine)

with open (pathFileHourly,'w') as currentFile:
  for i in range(len(overwrite)):
    currentFile.write(overwrite[i])

if nowHour==18:
  os.system('cat /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay)+'/hourlyResult_*'+' > /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay)+'/'+fileDaily)
  os.system('hdfs dfs -mkdir -p outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay))
  os.system('hdfs dfs -put ../outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay)+'/'+fileDaily+' outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+str(nowMonth)+'-'+str(nowDay))

  if now.weekday() == 4 :
    os.system('python /home/alumno/bigdatapracticas/proyecto/scripts/proyecto_data.py /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/*/dailyResult_* > /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+fileWeekly)
    os.system('hdfs dfs -put ../outputs/'+str(nowYear)+'/'+str(nowWeek)+'/'+fileWeekly+' outputs/'+str(nowYear)+'/'+str(nowWeek))
    
    os.system('python /home/alumno/bigdatapracticas/proyecto/scripts/proyecto_data.py /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/*/'+str(nowMonth)+'-*/dailyResult_* > /home/alumno/bigdatapracticas/proyecto/outputs/'+str(nowYear)+'/'+fileMonthly)
    os.system('hdfs dfs -put ../outputs/'+str(nowYear)+'/'+fileMonthly+' outputs/'+str(nowYear))