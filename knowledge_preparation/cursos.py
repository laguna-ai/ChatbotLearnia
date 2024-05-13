import pandas as pd
import csv

# Cargar el archivo CSV con el delimitador correcto y manejo de comillas
file_path = "cursos.csv"
df = pd.read_csv(
    file_path, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL, encoding="utf-8"
)

# Transformar el dataframe al formato deseado
melted_df = df.melt(id_vars=["Nombre"], var_name="campo", value_name="contenido")

# Renombrar las columnas para que coincidan con el formato de salida deseado
melted_df.rename(columns={"Nombre": "nombre del curso"}, inplace=True)

# Guardar el dataframe transformado en un nuevo archivo CSV
output_file_path = "csv_conocimientos/cursos.csv"
melted_df.to_csv(output_file_path, index=False)
