import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

PolyModel = ""
PolyModel2 = ""

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

  PolyModel = np.poly1d(np.polyfit(x_Pre_train, y_Pre_train, 3))

  myline = np.linspace(0, 24, 100)

  print("PRED", PolyModel(18))
  
  plt.scatter(x_Pre_train, y_Pre_train)
  plt.plot(myline, PolyModel(myline))

  # plt.show()

  ## Despues de comer

  PolyModel2 = np.poly1d(np.polyfit(x_Post_train, y_Post_train, 5))

  myline2 = np.linspace(0, 24, 100)

  print("PRED", PolyModel2(18))
  
  plt.scatter(x_Post_train, y_Post_train)
  plt.plot(myline2, PolyModel2(myline2))

  plt.show()


