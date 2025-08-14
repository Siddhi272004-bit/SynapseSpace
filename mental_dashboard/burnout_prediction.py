import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report 
import pickle
import numpy as np
from imblearn.over_sampling import SMOTE
import joblib


# load the dataset:
df=pd.read_csv('mental_health_workplace_survey.csv')

df = pd.get_dummies(df, columns=['Gender','HasTherapyAccess','RemoteWork'], drop_first=True)

# preprocessing:
# df=df.drop(columns=['BurnoutRisk'])

df['Energy']=(df['SleepHours']*0.4)+(df['PhysicalActivityHrs']*0.3)-(df['StressLevel']*0.3)-(0.1*df['MentalHealthDaysOff'])

df['Focus']=(df['JobSatisfaction']*0.3)+(df['ProductivityScore']*0.3)-(df['BurnoutLevel']*0.2)+((60-abs(df['WorkHoursPerWeek']-45))/60)

df['Motivation'] = (
    0.25 * df['CareerGrowthScore'] +
    0.25 * df['ManagerSupportScore'] +
    0.2 * df['WorkLifeBalanceScore'] +
    0.15 * np.where(df['HasMentalHealthSupport'] == 'Yes', 1, 0) +
    0.15 * df.get('HasTherapyAccess_Yes', 0)
)

# defining the input and target features
final_features = ['Age', 'SleepHours', 'Energy', 'Focus', 'Motivation', 'JobSatisfaction', 
                  'StressLevel', 'ManagerSupportScore', 'RemoteWork_Yes', 'TeamSize', 'WorkHoursPerWeek']

X = df[final_features]
y = df['BurnoutRisk']             # labels (what we want to predict)

# train-test-split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)
# model:
burnout_model = RandomForestClassifier(class_weight='balanced', random_state=42)
burnout_model.fit(X_resampled,y_resampled)

y_pred = burnout_model.predict(X_test)


joblib.dump(burnout_model, 'burnout_model.joblib')



