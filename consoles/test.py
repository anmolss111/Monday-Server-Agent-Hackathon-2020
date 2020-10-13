import requests

headers = {

    'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjg3NTMyMTk5LCJ1aWQiOjE2MzMzNDg1LCJpYWQiOiIyMDIwLTEwLTA4VDE2OjQ3OjE3LjAwMFoiLCJwZXIiOiJtZTp3cml0ZSJ9.1vga67sdYDdejaw7eeQDdLsWHfwUdrerSsCKAGVf5E8',
    'Content-Type' : 'application/json'
}

data = '''
    {
        "query" : "{ items (ids: [790136561,790136562]) { name, column_values { id, text, value, title, type } } }"
    }
    '''

r = requests.post('https://api.monday.com/v2/', headers = headers, data = data)
print(r.json())
