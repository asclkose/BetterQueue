import requests
import openai
import csv
import re

from itertools import islice

chatgptprompt = "Give a 3-10 word title that summarize the following given prhase, without using numbers:"
chatgptprompt2 = "Given the title of the conversation '"
chatgptprompt2_1 = "', rate on a scale of 1-9 in a list format, to a list of other titles of conversations on how likely the conversations would be similar to each other: "

ianum = 6
ialist = dict()

class openaicalls:
    openai.api_key = "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"
    def apicall(self, inputprompt, userid):
        completion = openai.Completion.create(
            engine="text-davinci-003", prompt=inputprompt, max_tokens=1000)
        if (len(ialist) < 6):
            tempinput = str(completion.choices[0]['text'].strip())
            tempinput = (tempinput.replace(
                ":", "").replace(".", "").replace("\"", "").replace("-", "").replace("\n","")).strip()
            ialist[tempinput] = [userid]
        else:
            alltitles = ""
            for key in ialist.keys():
                alltitles += key.strip() + ", "
            newtitle = ((completion.choices[0]['text']).replace(
                ":", "").replace(".", "").replace("\"", "").replace("-", "")).strip()
            newprompt = chatgptprompt2 + newtitle + chatgptprompt2_1 + alltitles
            newcompletion = openai.Completion.create(
                engine="text-davinci-003", prompt=newprompt, max_tokens=1000)
            newoutputstring = (newcompletion.choices[0]['text']).splitlines()
            highestoutputstring = ""
            highestoutputvalue = -1
            for lines in newoutputstring:
                if len(lines) != 0 and lines[-1].isdecimal():
                    if (int(lines[-1]) > highestoutputvalue):
                        highestoutputvalue = int(lines[-1])
                        highestoutputstring = re.sub(
                            r'\d', '', lines)
                        highestoutputstring = (highestoutputstring.replace(
                            ":", "").replace(".", "").replace("\"", "").replace("-","")).strip()
            if highestoutputstring in ialist:
                if (highestoutputstring > 8):
                    ialist[highestoutputstring].append(userid)
            

base_url = 'https://api.wix.com/v1/'
site_name = 'https://billbob1702.wixsite.com/my-site'
collection_name = 'WorkingQueueDataBase'

api_key = 'gRsGN6ppaKdT3'
headers = {'Content-Type': 'application/json', 'x-wix-access-token': api_key}

collection_id_url = f'{site_name}/collections/{collection_name}'
collection_response = requests.get(collection_id_url, headers=headers)
collection_id = collection_response.json()['id']

items_url = f'{base_url}collections/{collection_id}/items'
items_response = requests.get(items_url, headers=headers)
items = items_response.json()['items']

input = []

for item in items:
    input.append(item)

currentcall = openaicalls()

#with open('output.csv', 'r') as input_file:
    #reader = csv.reader(input_file) #should include user id 
for values in input: 
    tempuserid = 0
    for row in islice(values, 7):
        chatgptprompt = chatgptprompt+row[0]
        currentcall.apicall(chatgptprompt, tempuserid)
        tempuserid += 1

for item in items:
    item_id = item['_id']
    update_url = f'{base_url}collections/{collection_id}/items/{item_id}'
    data = {"title": "New Title", "description": "New Description"}
    update_response = requests.patch(update_url, json=data, headers=headers)
    if update_response.status_code == 200:
        print(f'Item {item_id} updated successfully')
    else:
        print(f'Error updating item {item_id}')
