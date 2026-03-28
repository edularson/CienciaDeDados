import pandas as pd
import matplotlib.pyplot as plt

#ler dados
failures = pd.read_csv('FalenciaBancos.csv', sep=',', encoding='latin-1')

# limpar nomes das colunas
failures.columns = failures.columns.str.replace('\xa0', '', regex=True).str.strip()

#ver colunas
print(failures.columns)

#agora existe
close_timestamps = pd.to_datetime(failures["Closing Date"], errors='coerce')
close_timestamps = close_timestamps.dropna()

#contagem por ano
failures_by_year = close_timestamps.dt.year.value_counts().sort_index()

#plot
failures_by_year.plot(kind='bar')
plt.xlabel("Ano")
plt.ylabel("Numero de falencia")
plt.title("Falencias bancarias por ano")
plt.show()