APPId = ""
APIKey = ""
APISecret = ""

# 请求数据
request_data = {
	"header":{
		"app_id":"123456",
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
			"image":"./resource/input/image/阳光总在风雨后.jpg",
			"status":3
		}
	}
}

# 请求地址
request_url = "https://cn-global.xf-yun.com/v1/private/sd8d91557"

# 用于快速定位响应值

response_path_list = ['$..payload.recognition', ]