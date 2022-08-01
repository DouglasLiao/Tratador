import pandas as pd  
  
data = pd.read_csv('dados.csv')
print("Dados sem tratar")
print(data.to_string())

data = data.drop([
    "group",
    "variable",
    "type",
    "value",
    "unit",
    "location",
    "metadata",
    "time",
    "created_at",], axis=1)

df = data['id'].str.split(',', expand=True, n=6)

df.columns = [
    "Dado1", 
    "Dado2", 
    "Dado3", 
    "Dado4",
    "Dado5", 
    "Dado6", 
    "Dado7",
 ]

df = df.drop([
    "Dado1", 
    "Dado2", 
    "Dado3", 
    "Dado4",
    # "Dado5", 
    "Dado6",
    "Dado7"
], axis=1)

df = df['Dado5'].str.split(' ', expand=True, n=1)

print("Dados tratados")
print(df.to_string(header=False)) 

df.to_csv('dados_tratados.csv', index=True, header=False)