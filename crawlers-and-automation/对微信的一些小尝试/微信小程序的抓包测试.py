import requests
import certifi
from urllib.parse import quote


def add_subscriber():
    print("=== 订阅用户信息录入 ===")

    # 用户输入
    name = input("请输入姓名：")
    id_card = input("请输入身份证号(18位)：").strip()

    # 验证身份证长度
    while len(id_card) != 18:
        print("身份证号必须是18位！")
        id_card = input("请重新输入身份证号：").strip()

    # 请求URL
    url = "https://m.msyc.cc/subscribers/add"

    # 请求头
    headers = {
        "Host": "m.msyc.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/13487",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://servicewechat.com/wx74c2d5974cb51e51/204/page-frame.html",
        "X-Web-XHR": "1",
        "Accept": "*/*"
    }

    # 请求数据（使用用户输入）
    data = {
        "cid": id_card,  # 使用身份证作为cid
        "name": (name),  # URL编码姓名
        "sodId": "",
        "msToken": "eyJhbGciOiJIUzI1NiJ9.eyJpc01hbmFnZSI6ZmFsc2UsImNsaWVudCI6IldYTUlOSSIsIm1lbWJlclR5cGUiOjQsInVzZXJOYW1lIjoiIiwiZXhwIjo3Nzc2MDAwMDAwLCJpYXQiOjE3NDY0NTQ3NzQ3NjYsInVzZXJLZXkiOjE3NzkxMjAyfQ.-BxkLKNMEuVR4NU4R5JJC0xJA3GuJbQ9GJ3RuHPkzrg",
        "uid": "17791202",
        "tmn": "754689",
        "tmnId": "754689",
        "client": "WXMINI",
        "wx_version": "5.1",
        "device_id": "o8fTq0BwLBGqzYIiN01ZRw8yHJrU",
        "second_client": "5"
    }

    try:
        print("\n正在提交数据...")

        # 尝试使用证书验证
        response = requests.post(
            url,
            headers=headers,
            data=data,
            verify=False,
            timeout=10
        )

        print(f"\n请求成功！状态码: {response.status_code}")
        print("响应内容:", response.text)

    except requests.exceptions.SSLError:
        print("\nSSL证书验证失败，尝试不验证证书...")
        try:
            response = requests.post(
                url,
                headers=headers,
                data=data,
                verify=False,
                timeout=10
            )
            print(f"\n请求成功(不验证证书): {response.status_code}")
            print("响应内容:", response.text)
        except Exception as e:
            print("\n最终请求失败:", str(e))

    except Exception as e:
        print("\n请求发生错误:", str(e))


if __name__ == "__main__":
    add_subscriber()
    input("\n按Enter键退出...")