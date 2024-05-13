import pandas as pd
import json

# Load the CSV file
file_path = 'Q&A.csv'
data = pd.read_csv(file_path)

# Initialize a list to hold the JSON output
json_output = []

# Iterate over columns starting from the second column
for column in data.columns[1:]:
    # Extract the question from the column header
    question = column
    
    # Extract the three answers from the column values
    answers = data[column].dropna().tolist()
    
    # Append the question and answers to the JSON output list
    json_output.append({
        "pregunta": question,
        "respuestas": answers
    })

n=len(json_output)
print(f"Número de preguntas/repuestas: {n}")

for i in range(n):
    print(json_output[i])   
