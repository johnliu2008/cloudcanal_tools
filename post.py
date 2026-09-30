import requests
import json
from requests_toolbelt import MultipartEncoder
import config
import authenticate
import cloudcanal_api_request


def _public_params():
    # 动态签名，失败时重试一次（首次调用偶发 497 签名错误）
    try:
        return authenticate.unquoted_public_params()
    except Exception:
        return authenticate.unquoted_public_params()


def send_post_request_json(cc_number, api_path, request_data):
    try:
        public_params = _public_params()
        endpoint = config.CC_endpoint_str.format(Number=cc_number)
        url = endpoint + api_path + '?%s' % public_params  # 拼接完整的 API URL
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=request_data, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            # print("POST request successful!")
            # print("Response:")
            # print(response.json())  # 输出响应内容
            return response.json()
        else:
            print(f"POST request failed with status code {response.status_code}")
            print("Response:")
            print(response.text)  # 输出响应内容（错误信息）
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def send_post_request_data(cc_number, api_path, request_data):
    try:
        public_params = _public_params()
        endpoint = config.CC_endpoint_str.format(Number=cc_number)
        url = endpoint + api_path + '?%s' % public_params  # 拼接完整的 API URL

        m = MultipartEncoder(
            fields=request_data
        )

        response = requests.post(url, data=m, headers={'Content-Type': m.content_type})

        # 检查响应状态码
        if response.status_code == 200:
            return response.json()
        else:
            print(f"POST request failed with status code {response.status_code}")
            print("Response:")
            print(response.text)  # 输出响应内容（错误信息）
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
