# from django.test import TestCase

# # Create your tests here.


import requests

url = 'https://api.fpt.ai/hmi/tts/v5'

payload = 'Phú đã điểm danh thành công'
headers = {
    'api-key': 'ojp4yPxFFpuNozefkke0ZrSQt5SXR55W',
    'speed': '',
    'voice': 'banmai'
}

response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

print(response.text)