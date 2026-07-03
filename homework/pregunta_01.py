"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd


def crea_dataframe():
    
    file_path = "files/input/clusters_report.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clusters = []
    current_cluster = None

    for line in lines:
        if not line.strip() or "---" in line or "Cluster" in line:
            continue

        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)

        if match:
            if current_cluster:
                clusters.append(current_cluster)

            current_cluster = {
                "cluster": int(match.group(1)),
                "cantidad_de_palabras_clave": int(match.group(2)),
                "porcentaje_de_palabras_clave": float(
                    match.group(3).replace(",", ".")
                ),
                "principales_palabras_clave": match.group(4).strip(),
            }
        else:
            if current_cluster:
                current_cluster["principales_palabras_clave"] += (
                    " " + line.strip()
                )

    if current_cluster:
        clusters.append(current_cluster)

    df = pd.DataFrame(clusters)

    def normalizar_keywords(text):
        if text.endswith("."):
            text = text[:-1]

        words = text.split(",")
        cleaned_words = [" ".join(w.split()) for w in words]
        return ", ".join([w for w in cleaned_words if w])

    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        normalizar_keywords
    )

    return df

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    df = crea_dataframe()

    return df
print(pregunta_01())
