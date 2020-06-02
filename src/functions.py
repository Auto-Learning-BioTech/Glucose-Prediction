import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

from csv import writer
from datetime import date

import json


PolyModel = None
PolyModel2 = None

def TrainLR(data):

  # 48 = 57 = Unspecified blood glucose measurement
  # 58 = Pre-breakfast blood glucose measurement
  # 59 = Post-breakfast blood glucose measurement
  # 60 = Pre-lunch blood glucose measurement
  # 61 = Post-lunch blood glucose measurement
  # 62 = Pre-supper blood glucose measurement
  # 63 = Post-supper blood glucose measurement
  # 64 = Pre-snack blood glucose measurement

  x_Pre_train = np.array([])
  y_Pre_train = np.array([])

  x_Post_train = np.array([])
  y_Post_train = np.array([])

  # Obtenemos solo los codigos con los que vamos a trabajar
  for row in data:

    code = row.get('code')

    if code == 58 or code == 60 or code == 62 or code == 64:
      x_Pre_train = np.append(row.get('hour'), x_Pre_train)
      y_Pre_train = np.append(row.get('glucose'), y_Pre_train)

    if code == 59 or code == 61 or code == 63:
      x_Post_train = np.append(row.get('hour'), x_Post_train)
      y_Post_train = np.append(row.get('glucose'), y_Post_train)


  ### POLYNOMIAL REGRESSION

  ## Antes de comer

  global PolyModel
  PolyModel = np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, 5))

  ## Despues de comer

  global PolyModel2
  PolyModel2 = np.poly1d(np.polyfit(x_Post_train, y_Post_train, 5))

def PredictLR(hour):

  if PolyModel is not None and PolyModel2 is not None:

    result = {
      'antes_de_comer':PolyModel(hour),
      'despues_de_comer':PolyModel2(hour),
    }

    return result
    #return 'Antes de comer: ' + str(PolyModel(hour)) + '\nDespues de comer: ' +  str(PolyModel2(hour))

  else:

    return 'El modelo no ha sido entrenado'

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

#Indicates whether to alert or not the user of high glucose levels
def GetStatus(hour):
  prediction = PredictLR(hour)

  beforeEating = prediction['antes_de_comer']
  afterEating = prediction['despues_de_comer']

  if(beforeEating > 200 or afterEating > 200):
    return 'notify'
  else:
    return 'do not notify'

def get_data_from_csv(csv_name):

  # Get date of today
  today = date.today()
  month = today.month
  day = today.day

  data = []

  a = 1

  # Open file in read mode
  with open('./src/intermediate_dataset/'+csv_name, 'r') as write_obj:
    for line in write_obj:

      line = line.split(',')

      # get csv day
      csv_month = int(line[0])
      # get csv month
      csv_day = int(line[1])
      # get csv hour
      csv_hour = int(line[2])
      # get csv gloucose
      csv_g = int(line[3])

      if month == csv_month and csv_day > (day-7) and csv_day <= day:
        a += 1

        data.append({"hour": csv_hour, "level": csv_g})

  return data

def TrainPoly(data):
  #Declare necesary arrays
  polyCooefficients = []
  x_Pre_train = np.array([])
  y_Pre_train = np.array([])

  # x_Post_train = np.array([])
  # y_Post_train = np.array([])

  #Declare necesary variables
  maxpoly = 30
  PolyModelsPre = []
  PolyModelsPost = []
  bestModelIndex = -1
  bestscore = 100000000

  dayprev = 0
  day = 0
  count = 0
  #Feed Data into arrays
  for row in data:
    # day = int(row.get('day'))
    # if dayprev == 0:
    #   dayprev = int(row.get('day'))
    #   day = int(row.get('day'))
    #   x_Pre_train = np.append(int(row.get('hour')), x_Pre_train)
    #   y_Pre_train = np.append(int(row.get('level')), y_Pre_train)
    # elif dayprev == day:
    #   x_Pre_train = np.append(int(row.get('hour')), x_Pre_train)
    #   y_Pre_train = np.append(int(row.get('level')), y_Pre_train)
    # elif dayprev < day:
    #   count += 1
    #   x_Pre_train = np.append(int(row.get('hour'))+ 24*count, x_Pre_train)
    #   y_Pre_train = np.append(int(row.get('level')), y_Pre_train)
    # prevday = day

    x_Pre_train = np.append(int(row.get('hour')), x_Pre_train)
    y_Pre_train = np.append(int(row.get('level')), y_Pre_train)


  #Model creation
  print(x_Pre_train)
  print(y_Pre_train)


  for i in range(maxpoly):
    PolyModelsPre.append( np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i)))
    # PolyModelsPost[i] = np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i))
    score = 0
    for j in range(x_Pre_train.size):
      score += abs(PolyModelsPre[i](x_Pre_train[j]) - y_Pre_train[j])
    # print(score)
    if score < bestscore:
      bestscore = score
      bestModelIndex = i

  polyCooefficients = PolyModelsPre[bestModelIndex].c
  
  return polyCooefficients

def RetrainPoly(polyCooefficients, data):
  newPolyCooefficients = []
  originalModel = np.poly1d(polyCooefficients)

  #Declare necesary arrays
  x_Pre_train = np.array([])
  y_Pre_train = np.array([])

  # x_Post_train = np.array([])
  # y_Post_train = np.array([])

  #Declare necesary variables
  maxpoly = 30
  PolyModelsPre = []
  PolyModelsPost = []
  bestModelIndex = -1
  bestscore = 100000000

  #Feed Data into arrays
  for i in range(13):
    x_Pre_train = np.append(i)
    y_Pre_train = np.append(originalModel(i))
  for row in data:
    x_Pre_train = np.append(row.get('hour'), x_Pre_train)
    y_Pre_train = np.append(row.get('level'), y_Pre_train) 



  for i in range(maxpoly):
    PolyModelsPre.append( np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i)))
    # PolyModelsPost[i] = np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i))
    score = 0
    for j in range(x_Pre_train.size):
      score += abs(PolyModelsPre[i](x_Pre_train[j]) - y_Pre_train[j])
    # print(score)
    if score < bestscore:
      bestscore = score
      bestModelIndex = i

  newPolyCooefficients = PolyModelsPre[bestModelIndex].c

  return newPolyCooefficients
  newPolyCooefficients = []
  originalModel = np.poly1d(polyCooefficients)

  #Declare necesary arrays
  x_Pre_train = np.array([])
  y_Pre_train = np.array([])

  # x_Post_train = np.array([])
  # y_Post_train = np.array([])

  #Declare necesary variables
  maxpoly = 30
  PolyModelsPre = []
  PolyModelsPost = []
  bestModelIndex = -1
  bestscore = 100000000

  #Feed Data into arrays
  for row in data:
    x_Pre_train = np.append(int(row.get('hour'), x_Pre_train))
    y_Pre_train = np.append(int(row.get('level'), y_Pre_train))    

  for i in range(maxpoly):
    PolyModelsPre[i].append( np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i)))
    # PolyModelsPost[i] = np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, i))
    score = 0
    for j in range(x_Pre_train.size):
      score += PolyModelsPre[i](j) - y_Pre_train[j]
    if score < bestscore:
      bestscore = score
      bestModelIndex = i

  newPolyCooefficients = PolyModelsPre[bestModelIndex].c

  return newPolyCooefficients

def csv_to_jsonNew(data):
  json_data = {
    "username":"Chris",
    "data":[]
  }
  for info in data:
        year = info['year']
    month = info['month']
    day = info['day']
    hour = info['hour']
    level = info['level']
    json_data["data"].append({"year":year, "month":month, "day":day, "hour":hour, "level":level})

  return json_data

def csv_to_jsonOld(data):
  json_data = {
    "username":"Chris",
    "data":[]
  }
  for info in data:
    year = info.get('year')
    month = into.get('month')
    day = info.get('day')
    hour = info.get('hour')
    level = info.get('level')
    json_data["data"].append({"year":year, "month":month, "day":day, "hour":hour, "level":level})


  return json_data