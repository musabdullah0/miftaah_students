import requests
import json
import pandas as pd
import time

df_users = pd.DataFrame()
df_classes = pd.DataFrame()
df_classes_enrolled = pd.DataFrame()

### User API

method = "get"
url = f"https://miftaahinstitute.neolms.com/api/v2/users?api_key=34549ae698ce0b382e904b7a4c79a44a9da06059e7ec4f4cea7a&$limit=2500"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

rsp = requests.get(url, headers=headers)

df_users = pd.concat([df_users, pd.DataFrame(rsp.json()['data'])], 
                  ignore_index = True, verify_integrity = True)

df_users['full_name'] = df_users['first_name'] + ' ' + df_users['last_name']
df_users = df_users.rename(columns={"id": "student_user_id"})
df_users = df_users[['student_user_id', 'email', 'full_name', 'joined_at']]

### Classes API

method = "get"
url = f"https://miftaahinstitute.neolms.com/api/v2/classes?api_key=34549ae698ce0b382e904b7a4c79a44a9da06059e7ec4f4cea7a"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

rsp = requests.get(url, headers=headers)

df_classes = pd.concat([df_classes, pd.DataFrame(rsp.json()['data'])], 
                  ignore_index = True, verify_integrity = True)

df_classes = df_classes.rename(columns={"id": "class_id"})
df_classes = df_classes[['class_id', 'name', 'credits', 'start_at', 'finish_at']]

### Classes Enrolled API

for id in df_users['student_user_id'].tolist():
    method = "get"
    url = f"https://miftaahinstitute.neolms.com/api/v2/users/{id}/classes_enrolled?api_key=34549ae698ce0b382e904b7a4c79a44a9da06059e7ec4f4cea7a"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    rsp = requests.get(url, headers=headers)

    df_classes_enrolled = pd.concat([df_classes_enrolled, pd.DataFrame(rsp.json()['data'])], 
                      ignore_index = True, verify_integrity = True)

    df_classes_enrolled = df_classes_enrolled.drop_duplicates(subset=['id'])
    time.sleep(0.05)

df_classes_enrolled = df_classes_enrolled[['id', 'student_user_id', 'class_id', 'enrolled_at', 'enroll_type', 'percent', 'grade', 'progress', 'started_at', 'completed_at', 'unenrolled']]

df_merge_test = df_classes_enrolled.merge(df_classes,on='class_id').merge(df_users,on='student_user_id')
df_merge_test = df_merge_test.drop_duplicates(subset=['id'])
df_merge_test.to_csv('Merge Test.csv')