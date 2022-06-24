import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import regex as re
import json
import requests


def get_data(url: str) -> list:
    responses = []
    while url:
        url = requests.get(url)
        if url.status_code == 200:
            url = url.json()
            responses.append(url)
            url = url["nextPage"]
            print(f"Downloading: {url}")
        else:
            print("Error while accessing API")
    print("Download complete")
    return responses

    
#get all subject headings - specify: query string - 1. argument; header (subject, subjectCategory etc.) - 2. argument; marc21 field numbers - 3. argument

def get_subj(sub: str, header: str = "subjectCategory", field_numbers: list = ["150"]) -> dict:  
    responses = get_data(f"http://data.bn.org.pl/api/authorities.json?{header}={sub}")
    subjects = []
    for response in responses:
        for authority in response["authorities"]:
            for field in authority["marc"]["fields"]:
                for field_number in field_numbers:
                    if field_number in field:
                        for i in field:
                            subjects.append(list(field[i]["subfields"][-1].values())[0])
                
    subjects_dict = {}
    subjects_dict[sub] = subjects
    json_object = json.dumps(subjects_dict, indent = 4, ensure_ascii=False).encode("utf8")
    return json_object.decode()


