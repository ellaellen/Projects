
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

in_dir = "../data/raw_data/"
out_dir = ['./train', './test','./validation']
for out in out_dir:
    if not os.path.exists(out):
        os.mkdir(out)

patients = pd.read_csv(os.path.join(in_dir, 'PATIENTS.csv'))
admissions = pd.read_csv(os.path.join(in_dir, 'ADMISSIONS.csv'))
icustays = pd.read_csv(os.path.join(in_dir, 'ICUSTAYS.csv'))
diagnoses_icd = pd.read_csv(os.path.join(in_dir, "DIAGNOSES_ICD.csv"))


icustays = icustays.dropna(axis=0, subset=['LOS'])

icustays = icustays[icustays.LOS <= 1] # within 24hr

patients_icustays_24hr = icustays.groupby(['SUBJECT_ID']).count().reset_index()


patients_train, patients_test = train_test_split(patients_icustays_24hr, test_size = 0.2, random_state = 6250)
patients_train, patients_validation = train_test_split(patients_train, test_size = 0.2, random_state = 6250)



patients_id_train = patients_train[['SUBJECT_ID']]
patients_id_validation = patients_validation[['SUBJECT_ID']]
patients_id_test = patients_test[['SUBJECT_ID']]


admissions_train = pd.merge(admissions, patients_id_train)
admissions_validation = pd.merge(admissions, patients_id_validation)
admissions_test = pd.merge(admissions, patients_id_test)


diagnoses_icd_train = pd.merge(diagnoses_icd, patients_id_train)
diagnoses_icd_validation = pd.merge(diagnoses_icd, patients_id_validation)
diagnoses_icd_test = pd.merge(diagnoses_icd, patients_id_test)


patients_24hr_train = pd.merge(patients, patients_id_train)
patients_24hr_validation = pd.merge(patients, patients_id_validation)
patients_24hr_test = pd.merge(patients, patients_id_test)


mortality_train = patients_24hr_train[['SUBJECT_ID', 'EXPIRE_FLAG']]
mortality_train.columns = [['SUBJECT_ID', 'MORTALITY']]


mortality_test = patients_24hr_test[['SUBJECT_ID', 'EXPIRE_FLAG']]
mortality_test.columns = [['SUBJECT_ID', 'MORTALITY']]



mortality_validation = patients_24hr_validation[['SUBJECT_ID', 'EXPIRE_FLAG']]
mortality_validation.columns = [['SUBJECT_ID', 'MORTALITY']]


diagnoses_icd_train.to_csv("train/DIAGNOSES_ICD.csv", index=False)
diagnoses_icd_validation.to_csv("validation/DIAGNOSES_ICD.csv", index=False)
diagnoses_icd_test.to_csv("test/DIAGNOSES_ICD.csv", index=False)



mortality_train.to_csv("train/MORTALITY.csv", index=False)
mortality_validation.to_csv("validation/MORTALITY.csv", index=False)
mortality_test.to_csv("test/MORTALITY.csv", index=False)


admissions_train.to_csv("train/ADMISSIONS.csv", index=False)
admissions_validation.to_csv("validation/ADMISSIONS.csv", index=False)
admissions_test.to_csv("test/ADMISSIONS.csv", index=False)









