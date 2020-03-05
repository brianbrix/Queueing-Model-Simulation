import datetime
import random
import pandas as pd
import numpy as np

patient_dict = []
s = np.random.poisson(1.5, 270)
time_string = "08:00:00"
time_object = datetime.datetime.strptime(time_string, '%H:%M:%S')
times_list_string = [time_string]
new_time_object = (time_object + datetime.timedelta(minutes=int(s[0])))
print(new_time_object)
times_list_string.append(str(new_time_object.time()))
for x in range(len(s) - 1):
    new_time_object += datetime.timedelta(minutes=int(s[x]))
    times_list_string.append(str(new_time_object.time()))
sorted_time_list = sorted(times_list_string)
first_patient_time_in = datetime.datetime.strptime(sorted_time_list[0], '%H:%M:%S') + datetime.timedelta(
    minutes=random.randint(10, 30))
first_patient_time_out = datetime.datetime.strptime(str(first_patient_time_in.time()), '%H:%M:%S') + datetime.timedelta(
    minutes=random.randint(2, 5))
# second_patient_time_in = datetime.datetime.strptime(sorted_time_list[1], '%H:%M:%S') + datetime.timedelta(
#     minutes=random.randint(10, 30))
second_patient_time_out = datetime.datetime.strptime(str(first_patient_time_in.time()),
                                                     '%H:%M:%S') + datetime.timedelta(minutes=random.randint(2, 5))
x = 1
for time in sorted_time_list:
    details = {}
    details["patient"] = str(x)
    details["arrival"] = time
    patient_dict.append(details)
    x += 1
patient_dict[0]["time_in"] = str(first_patient_time_in.time())
patient_dict[0]["time_out"] = str(first_patient_time_out.time())
patient_dict[1]["time_in"] = str(first_patient_time_in.time())
patient_dict[1]["time_out"] = str(second_patient_time_out.time())
patient_dict[0]["doc"] = str(1)
patient_dict[1]["doc"] = str(2)
dd = [patient_dict[0]["time_out"], patient_dict[1]["time_out"]]
docs = [patient_dict[0]["doc"], patient_dict[1]["doc"]]
for d in range(2, len(patient_dict)):
    if patient_dict[d - 1]["doc"] != patient_dict[d - 2]["doc"]:
        patient_dict[d]["time_in"] = min(patient_dict[d - 1]["time_out"], patient_dict[d - 2]["time_out"])
    else:
        dd = sorted(dd)
        patient_dict[d]["time_in"] = dd[-2]
    patient_dict[d]["time_out"] = str((datetime.datetime.strptime(patient_dict[d]["time_in"],
                                                                  '%H:%M:%S') + datetime.timedelta(
        minutes=random.randint(2, 5))).time())
    if patient_dict[d - 1]["time_out"] < patient_dict[d - 2]["time_out"]:
        patient_dict[d]["doc"] = patient_dict[d - 1]["doc"]
    else:
        patient_dict[d]["doc"] = patient_dict[d - 2]["doc"]
    for x in range(len(dd)):
        if dd[x] == max(dd):
            if docs[x] == str(1):
                patient_dict[d]["doc"] = str(2)
            else:
                patient_dict[d]["doc"] = str(1)
    docs.append(patient_dict[d]["doc"])
    dd.append(patient_dict[d]["time_out"])

df = pd.DataFrame.from_dict(patient_dict)
df.to_excel("output.xlsx", index=False)
