import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

from csv import writer

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

