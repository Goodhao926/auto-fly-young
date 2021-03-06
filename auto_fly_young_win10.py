import requests
from lxml import etree
import execjs
import time
import os
import win10toast
from recognition import predict
wlanacip = "183.3.151.148" #服务器IP 不需要修改
wlanuserip = "172.16.141.135" # 学校DHCP分配的IP
username = "1940706246"
password = "01043715"
try_num = 0
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
def auto_connect():
    global try_num
    global is_connect
    with requests.session() as sess:
        # 使用移动端的AG可能会减少下线率 Maybe
        sess.headers = {
            "User-Agent":'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36'
        }
        try:
            res = sess.get(f"http://125.88.59.131:10001/qs/index_gz.jsp?wlanacip={wlanacip}&wlanuserip={wlanuserip}")
            # 识别验证码
            url = "http://125.88.59.131:10001/common/image_code.jsp?time=" + str(time.time_ns())

            with open("tmp/tmp.jpg", "wb") as f:
                f.write(sess.get(url).content)

            code = predict("tmp/tmp.jpg")
            print(code)

            with open("RSA.js", 'r') as f:
                js_text = f.read()
                js = execjs.compile(js_text)
                rsa_code = js.call('encryption_', username, password, code)
            data = {
                "wlanacip": wlanacip,
                "wlanuserip": wlanuserip,
                "loginKey": rsa_code
            }
            res = sess.post("http://125.88.59.131:10001/ajax/login", data).json()
            if res['resultCode'] != "13002000":
                try_num += 1
                if try_num > 10:
                    print("连接失败")
                else:
                    auto_connect()

            else:
                if internet_test():
                    print("连接成功")
                    is_connect = True



        except:
            import traceback
            traceback.print_exc()
            print("连接失败，请检测网线")


def internet_test():
    res = os.system("ping www.baidu.com -n 1")
    return res == 0

if __name__ == '__main__':
    toast = win10toast.ToastNotifier()

    while True:
        if not internet_test():
            is_connect = False
            toast.show_toast(title="飞Young网络工具",msg="重新连接中...",duration=10)
            auto_connect()
            if is_connect:
                toast.show_toast(title="飞Young网络工具", msg="连接成功...", duration=10)

        time.sleep(2)


