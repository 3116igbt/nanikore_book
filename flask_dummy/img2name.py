from docomocv import DocomoCVClient
import requests

def recognize(img, num_of_candidates=1):
    result = requests.post(
        url=__build_url('recognize'),
        params={'APIKEY': "6150436e4e496d4b4f493170723374436530495552373477486e6c2f474d6250443953784336416e555835", 'recog': 'product-all', 'numOfCandidates': num_of_candidates},
        data=img,
        headers={'Content-Type': 'application/octet-stream'})
    result.raise_for_status()
    output=result.json()

    if 'candidates' in  output.keys():
        return output['candidates'][0]['detail']['itemName']

    return 'nai'
    

def recognizeTest(img_file, num_of_candidates=1):
    with open(img_file, mode='rb') as f:
        result = requests.post(
        url=__build_url('recognize'),
        params={'APIKEY': "6150436e4e496d4b4f493170723374436530495552373477486e6c2f474d6250443953784336416e555835", 'recog': 'product-all', 'numOfCandidates': num_of_candidates},
        data=f,
        headers={'Content-Type': 'application/octet-stream'})
        result.raise_for_status()
        output=result.json()

    if 'candidates' in  output.keys():
        return output['candidates'][0]['detail']['itemName']
        
    return 'nai'

def __build_url(name, version='v1'):
    return __api_path.format({'version': version, 'name': name})

def __valid_to_str(is_valid):
    return 'true' if is_valid else 'false'

__api_path = 'https://api.apigw.smt.docomo.ne.jp/imageRecognition/{0[version]}/{0[name]}'
