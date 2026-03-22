import pandas as pd

for bloco in pd.read_csv('dados_sensor_gigante.csv', chunksize=10):
    media_temperatura = bloco["temperatura"].mean()
    valores_faltando = bloco["temperatura"].isna().sum()
    print(bloco)
    print("temperatura media:", media_temperatura)
    print("valores faltando na temperatura:", valores_faltando)