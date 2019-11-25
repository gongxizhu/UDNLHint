import os, requests, uuid, json

subscriptionKey = '4665d07cbd15466db82440ec8b308952'
base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate(text_list, to_lang = 'en'):
    params = '&to=' + to_lang
    constructed_url = base_url + path + params
    body = []
    retults = []
    for text in text_list:
        item = {'text': text}
        body.append(item)
    # print(body)
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    print(response)
    for response_item in response:
        result = response_item['translations'][0]['text']
        retults.append(result)
    
    return retults

if __name__ == "__main__":
    senstences = ['エンジンオイルのみ交換 シャシグリスアップ クラッチ点検調整 エアエレメント清掃 バックモニター振動で切れる 部品 エンジン オイル、交換 シャーシ給脂、全グリスポイント クラッチ、調整 エアクリーナー フィルター インサート、清掃 バックモニター切れる点検'] 
    tranlated_text = translate(senstences)
    print(tranlated_text)