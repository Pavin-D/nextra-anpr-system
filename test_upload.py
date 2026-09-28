import requests

url = "http://localhost:8001/api/v1/upload-feeds"
files = {
    'cam1': ('test.mp4', b'dummy content', 'video/mp4')
}

response = requests.post(url, files=files)
print(response.status_code)
print(response.text)
