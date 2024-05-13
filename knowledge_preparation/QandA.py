import pandas as pd
import json
from RAG.Chat_Response import get_completion_from_messages

def get_QandA_extended(file_path = 'Q&A.csv'):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Initialize a list to hold the JSON output
    QandA_extended = []

    # Iterate over columns starting from the second column
    for column in data.columns[1:]:
        # Extract the question from the column header
        question = column
        
        # Extract the three answers from the column values
        answers = data[column].dropna().tolist()
        
        # Append the question and answers to the JSON output list
        QandA_extended.append({
            "pregunta": question,
            "respuestas": answers
        })

    n=len(QandA_extended)
    print(f"Número de preguntas/respuestas encontradas: {n}")
    return QandA_extended


def get_synth_template(question_and_responses):
    p=question_and_responses["pregunta"]
    [r1,r2,r3]=question_and_responses["respuestas"]
    template=f""" A continuación encontrarás una pregunta junto\
    junto con tres respuestas.
    ### 
    pregunta: {p}
    -respuesta1: {r1}
    -respuesta2: {r2}
    -respuesta3: {r3}
    ###
    Construye una única respuesta que resuma las tres respuestas.
    La respuesta debe ser de un sólo párrafo y tener la información esencial\
    y factual de las tres respuestas, sin salirse del contexto de éstas.
    """
    return template


def get_synth_responses(QandA_extended):
    faqs = []
    for item in QandA_extended:
        prompt = {"role": "system", "content": get_synth_template(item)}
        response = get_completion_from_messages([prompt])[0]  # Assuming the response is in the first element
        faqs.append({
            "pregunta": item["pregunta"],
            "respuesta": response
        })
    
    # Convert the list of FAQs to a DataFrame
    faqs_df = pd.DataFrame(faqs)

    # Save the DataFrame to a CSV file
    output_file_path = 'FAQ.csv'
    faqs_df.to_csv(output_file_path, index=False)
    print(f"CSV file {output_file_path} has been created successfully.")

# Example usage

QandA_extended = get_QandA_extended('Q&A.csv')
get_synth_responses(QandA_extended)

