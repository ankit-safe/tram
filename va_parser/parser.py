﻿import json
import os
import re

import requests

# cve = "CVE-2022-0100"


# with open("/Users/ankitchauhan/Documents/va_parser/tsar.json", "r") as f:
#     data = json.load(f)

# for year in range(2022, 2000, -1):
#     year = str(year)

#     temp_dict = {}
#     cve_data = []

#     for cve_key in data:

#         reg_ex = re.search("CVE-" + year + "-", cve_key)

#         if reg_ex != None:
#             temp_dict[cve_key] = data[cve_key]
#             cve_data.append(temp_dict)
#             temp_dict = {}

#     with open(
#         "/Users/ankitchauhan/Drive/tram/va_parser/year-wise-cves/CVE_" + year + ".json",
#         "w",
#     ) as json_file:
#         json.dump(cve_data, json_file, indent=4)


def get_technique_name(technqiue_id):

    attack_path = os.getcwd() + "/va_parser/attack-technique/"
    file_path = os.path.join(attack_path, technqiue_id + ".json")

    technique_list = os.listdir(attack_path)

    if technqiue_id + ".json" in technique_list:

        with open(file_path, "r", encoding="utf-8-sig") as f:
            technique_data = json.load(f)

        return technique_data["name"]
    return ""


year = 2022

count = 0

path = os.getcwd() + "/va_parser/year-wise-cves/"

filename = "CVE_" + str(year) + ".json"

file_path = path + filename

with open(file_path, "r") as f:
    cve_data = json.load(f)

url = "http://localhost:8000/techniques/"


for single_cve in cve_data:

    cve_path = os.getcwd() + "/va_parser/cve-data/"

    exported_cve_list = os.listdir(cve_path)

    cve_id = list(single_cve.keys())[0]

    if cve_id + ".json" not in exported_cve_list:

        print("Writing data for. . . ", cve_id)

        final_json = {}
        cve_desc = single_cve[cve_id]["title"]

        payload = json.dumps(
            [
                {
                    "unique_identifier": cve_id,
                    "description": [
                        {
                            "field_data": cve_desc,
                            "field_type": "control",
                        }
                    ],
                    "techniqueMapping": "",
                }
            ]
        )
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMzk2MDc5LCJpYXQiOjE2NjczOTYwNzksImp0aSI6IjcyNjU3YjI1MGNmNjQ2Y2U4MTQ2YTA3Y2Q4MWYzZDNhIiwidXNlcl9pZCI6Mn0.Qr2gdBgWJCut36ZA1Yft_xOJvTTq53ruQsSsIdfCWAA",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        ttp_mapping = json.loads(response.content)[0]["technique_list"]

        final_json = single_cve[cve_id]
        ttp_list = []

        for single_technique in ttp_mapping:
            temp_dict = single_technique
            technique_id = temp_dict["technique_id"]
            temp_dict["technique_name"] = get_technique_name(technique_id)
            ttp_list.append(temp_dict)

        final_json["ttpMapping"] = ttp_list

        out_path = os.getcwd() + "/va_parser/cve-data/"

        with open(
            out_path + cve_id + ".json",
            "w",
        ) as json_file:
            json.dump(final_json, json_file, indent=4)
        count += 1
        print(". . . . . ", count, " . . . . . ")
        print("Successfully wrote data for. . . ", cve_id)
