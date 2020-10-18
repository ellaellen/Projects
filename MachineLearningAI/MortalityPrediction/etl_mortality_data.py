import os
import pickle
import pandas as pd


path_train = "../data/mortality/train/"
path_validation = "../data/mortality/validation/"
path_test = "../data/mortality/test/"
path_output = "../data/mortality/processed/"


def convert_icd9(icd9_object):
   
    icd9_str =str(icd9_object)
    if icd9_str[0]=='E':
        return icd9_str[0:4]
    else:
        return icd9_str[0:3]


def build_codemap(df_icd9, transform):
    df_icd9=df_icd9.dropna()
    df_digits = df_icd9['ICD9_CODE'].apply(transform)
    icd9=df_digits.drop_duplicates()
    icd=icd9.tolist()
    ind=icd9.reset_index().index
    codemap=dict(zip(icd,ind))
    return codemap


def create_dataset(path, codemap, transform):
 
    df_mortality = pd.read_csv(os.path.join(path, "MORTALITY.csv"))
    df_admission = pd.read_csv(os.path.join(path, "ADMISSIONS.csv"))
    dfa=df_admission.loc[:,['HADM_ID','ADMITTIME']]
    dfa['DATE']=dfa['ADMITTIME'].str[:11]
    df_diag = pd.read_csv(os.path.join(path, "DIAGNOSES_ICD.csv"))
    df_diag_mort =pd.merge(df_diag,df_mortality,on='SUBJECT_ID',how='inner')
    df_diag_mort_adm =pd.merge(df_diag_mort,dfa,on='HADM_ID',how='inner')
    df=df_diag_mort_adm.loc[:, ['SUBJECT_ID','DATE','ICD9_CODE','MORTALITY']]
    df['ICD9']=df['ICD9_CODE'].apply(transform)
    df['ind'] =df['ICD9'].map(codemap)
    df=df.sort_values('SUBJECT_ID')
    df0= df.loc[:,['SUBJECT_ID', 'DATE',  'MORTALITY', 'ind']].dropna()
    df1=df0.groupby(['SUBJECT_ID','MORTALITY','DATE'],as_index=False)['ind'].apply(list)
    df2=pd.DataFrame(df1).reset_index()
    df3=df2.groupby(['SUBJECT_ID','MORTALITY'],as_index=False)[0].apply(list)
    df4=pd.DataFrame(df3).reset_index()
    patient_ids = list(df4['SUBJECT_ID'])
    labels = list(df4['MORTALITY'])
    seq_data = list(df4[0])
    return patient_ids, labels, seq_data



def main():
	# Build a code map from the train set
	print("Build feature id map")
	os.makedirs(path_output, exist_ok=True)    
	df_icd9 = pd.read_csv(os.path.join(path_train, "DIAGNOSES_ICD.csv"), usecols=["ICD9_CODE"])
	codemap = build_codemap(df_icd9, convert_icd9)
	pickle.dump(codemap, open(os.path.join(path_output, "mortality.codemap.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Train set
	print("Construct train set")
	train_ids, train_labels, train_seqs = create_dataset(path_train, codemap, convert_icd9)

	pickle.dump(train_ids, open(os.path.join(path_output, "mortality.ids.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_labels, open(os.path.join(path_output, "mortality.labels.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_seqs, open(os.path.join(path_output, "mortality.seqs.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Test set
	print("Construct test set")
	test_ids, test_labels, test_seqs = create_dataset(path_test, codemap, convert_icd9)

	pickle.dump(test_ids, open(os.path.join(path_output, "mortality.ids.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_labels, open(os.path.join(path_output, "mortality.labels.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_seqs, open(os.path.join(path_output, "mortality.seqs.test"), 'wb'), pickle.HIGHEST_PROTOCOL)


	# Validation set
	print("Construct validation set")
	validation_ids, validation_labels, validation_seqs = create_dataset(path_validation, codemap, convert_icd9)

	pickle.dump(validation_ids, open(os.path.join(path_output, "mortality.ids.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_labels, open(os.path.join(path_output, "mortality.labels.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_seqs, open(os.path.join(path_output, "mortality.seqs.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)

	print("Data processing completed!")


if __name__ == '__main__':
	main()
