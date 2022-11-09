from sample import ne_utils
from urllib import parse
from sample.aipass_client import prepare_req_data
import json
import requests
import base64
request_url="https://cn-huadong-1.xf-yun.com/v1/private/sd8d91557"
app_id="ab95be71"
api_key="7045abb15aeb925bb832a0f39735b011"
api_secret="NzcwYmJlOTNkYmE4OGJmYmRmM2YwNDBh"

request_data = {
	"header":{
		"app_id":app_id,
		"uid":"39769795890",
		"did":"SR082321940000200",
		"imei":"8664020318693660",
		"imsi":"4600264952729100",
		"mac":"6c:92:bf:65:c6:14",
		"net_type":"wifi",
		"net_isp":"CMCC",
		"status":3,
		"res_id":""
	},
	"parameter":{
		"sd8d91557":{
			"recognition":{
				"encoding":"utf8",
				"compress":"raw",
				"format":"json"
			}
		}
	},
	"payload":{
		"image":{
			"encoding":"jpg",
			"image":"./airplane.jpeg",
			"status":3
		}
	}
}


# 获取请求url
auth_request_url = ne_utils.build_auth_request_url(request_url, "POST", api_key, api_secret)

url_result = parse.urlparse(request_url)
headers = {'content-type': "application/json", 'host': url_result.hostname, 'app_id': app_id}
# 准备待发送的数据
new_request_data = prepare_req_data(request_data)
response = requests.post(auth_request_url, data=json.dumps(new_request_data), headers=headers)
print(response.content)

res_json=json.loads(response.content.decode("utf-8"))
real_data = base64.b64decode(res_json["payload"]["recognition"]["text"])
print(real_data)