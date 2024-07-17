import csv
from io import StringIO

def export_to_csv(data, fieldnames):
    """
    Exporta datos a un formato CSV.
    
    :param data: Lista de diccionarios con los datos a exportar
    :param fieldnames: Lista de nombres de campos para el CSV
    :return: String con el contenido CSV
    """
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return output.getvalue()