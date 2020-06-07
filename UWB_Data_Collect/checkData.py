import requests;

response = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")
an0011 ={}
data = {}
data = response.json()
an0011 = data["An0011"]
an0011 = eval(an0011)
for i in an0011.keys():
    print(i)