import pandas as pd 
import numpy as np
import math

df= pd.read_csv('/Users/rohinisaichandramunnangi/Downloads/Bank_Customer_Churn/Bank_Churn_Customer_info_Raw.csv')
print(df.columns)
print(df)
# inconsitstance in geography column, FRA, French onstead of French 

print(df['Geography'].unique())#['FRA' 'Spain' 'French' 'France' 'Germany'] 
# replace a column value with another 
#df_geography_updated = df['Geography'].replace('FRA','France')  
# replacing multiple values of same column in one go  with dict 
#geography_mapping={
#   'FRA':'France',
 #   'Germany':'Germany',
 #   'French':'France',
 #   'Spain':'Spain'
#}
#df['Geography']=df['Geography'].replace(geography_mapping) 
print(df['Geography'].unique()) #['FRA' 'Spain' 'French' 'France' 'Germany']
['France' 'Spain' 'Germany']
# (or) another way of replace mutiple values using and lists
df['Geography']=df['Geography'].replace(['FRA','French'],'France')
print(df['Geography'].unique()) # ['France' 'Spain' 'Germany']

df_gender_values=df['Gender'].unique()
print(df_gender_values) #['Female' 'Male']  
# customerId column has 10001 values . Findout how many were repeated/duplicated 
#all_customerId_repeated=df[df['CustomerId'].duplicated(keep=False)]
#print(all_customerId_repeated) 
print(df) # duplicates in customemriD has not been removed yet 
# 9999     15628319  Walker          792    France  Female  28.0  ...         NaN        NaN          NaN          NaN          NaN          NaN
#10000    15628319  Walker          792    France  Female  28.0  ...         NaN        NaN          NaN          NaN          NaN          NaN

# so 2 values are repeated . Now you have to drop them 
# Delete repeated rows based on the 'customer_id' column
# inplace=True updates your current dataframe directly 
#df=df.drop_duplicates(subset=['CustomerId'],keep='first',inplace=True) 
#Your code returns None because you combined inplace=True with an assignment operator (df = ...).
# In Python and Pandas, when you set inplace=True, you are telling the computer to modify your existing DataFrame directly 
# inside your computer's memory. Because it modifies the data "in place," the method does not generate a new DataFrame to hand 
# back—it returns None.By writing df = df.drop_duplicates(..., inplace=True), you took that None output and saved it over your 
# variable df, completely wiping out your dataset. 
df=df.drop_duplicates(subset=['CustomerId'],keep='first') 
print(df) # removed duplicated values in Customerid
columns_to_be_removed=['Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10',
       'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13']
df=df.drop(columns=columns_to_be_removed)
print(df) 
# check for missing_values in all columns  :# Count missing values in every column
df.isna()# shows which entries are missing :
print(df.isna().sum()) # print total no.of missing values per column 
missing_surnames_indices = df[df['Surname'].isna()].index.tolist() # shows whcih specific indexed hold the missing value . 
# this will be the same for age as well 
print(missing_surnames_indices) #[28, 121, 9389]
missing_age_indices = df[df['Age'].isna()].index.tolist() # shows whcih specific indexed hold the missing value 
print(missing_age_indices) #[28, 121, 9389] 
print(df.iloc[[28, 121, 9389]]) # printing the columns & rows with missing values 
# 1. Fill the missing Surnames with 'Unknown' across the WHOLE column
df['Surname']= df['Surname'].fillna('Unknown')   
print(df['Surname'].iloc[[28,121,9389]])
print(df.iloc[[121,28,9389]])
#handling age column : simply we cant replace with zero , so relace it with mean of age column , 
avg_mean= df['Age'].mean() 
df['Age']= df['Age'].fillna(avg_mean)
print(df['Age'].iloc[[28,121,9389]]) # 28      38.922077
#121     38.922077
#9389    38.922077  

# Handling NEgavtive Estimated Salary : Since a account holder cant have zero estimated salary with credit score>500. 
#This is a major risk flag and data integrity issue. 
# 1) So first filter the the rows with credit>500 and then find their median 
# (median is choosen over mean as mean colud give higher estimated salary as list could have millianires and their salary is
#  higher than rest which will result to higher mean values than normal )  

print(df['EstimatedSalary'].unique()) #<class 'pandas.core.series.Series'> 
#this means its string isntead of numbers 

df['EstimatedSalary'] = df['EstimatedSalary'].str.replace('€', '')

# 2. Convert the cleaned string column into a float (decimal number)
df['EstimatedSalary'] = df['EstimatedSalary'].astype(float) # this converts from string to float 
print(df['EstimatedSalary'].iloc[[28,121,9389]]) 
df['EstimatedSalary']=df['EstimatedSalary'].astype(str).str.replace(r'-\s*999999', 'NaN', regex=True)
df['EstimatedSalary'] = pd.to_numeric(df['EstimatedSalary'], errors='coerce')
print(df['EstimatedSalary'])
credit_above_500 = df['CreditScore']>=500 
median_salary=df[credit_above_500]['EstimatedSalary'].median()
print(median_salary) #100114.38500000001 
# now fill those -99999 with median salary 
df['EstimatedSalary']=df['EstimatedSalary'].fillna(median_salary)
print(df.iloc[[28,121,9389]]) 

print(df.isna())