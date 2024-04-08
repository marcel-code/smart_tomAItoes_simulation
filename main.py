import requests
import json

## MAIN SECTION

if __name__ == "__main__":

    # Test: passing control parameters to the model

    # select key
    key_A = 'SmartToms-A-gl4d-1cam' # key to simulator A
    key_B = 'SmartToms-B-gl4d-1cam' # key to simulator B
    key = key_A

    # read input json
    param_path = 'example_input.json'
    with open(param_path, 'r') as file:
        param = file.read()

    # simulator
    url = 'https://www.digigreenhouse.wur.nl/AGC2024/model/kaspro'
    data = {'key': key, 'parameters': json.loads(param)}
    response = requests.post(url, json=data) # https://realpython.com/python-requests/#the-response

    # print out the response
    print("Response:", response)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print("Response Content:", response.content)
    print("Response Reason:", response.reason)
    print("Response json:", response.json())
    
    # Write the response json to a file
    with open('response.json', 'w') as f:
        json.dump(response.json(), f)
