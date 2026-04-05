if __name__ == "__main__":
    import re
    
    with open("moduls/sms/services.py", "r", encoding="utf-8") as f:
        text = f.read()
    
    # Add import for Faker
    if "from faker import Faker" not in text:
        text = text.replace("import requests", "import requests\nfrom faker import Faker")
    
    # Add randomize() method and initialize Faker in __init__
    __init__pattern = r'def __init__\(self, phone, mail\):(.*?)(?=\n    #|\Z)'
    
    init_replacement = '''def __init__(self, phone, mail):
            self.fake = Faker("tr_TR")
            self.stealth_config = StealthConfig.from_level(STEALTH_FULL)
            self.randomize()
    
            rakam = []
            tcNo = ""
            rakam.append(randint(1,9))
            for i in range(1, 9):
                rakam.append(randint(0,9))
            rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
            rakam.append((rakam[0] + rakam[1] + rakam[2] + rakam[3] + rakam[4] + rakam[5] + rakam[6] + rakam[7] + rakam[8] + rakam[9]) % 10)
            for r in rakam:
                tcNo += str(r)
            self.tc = tcNo
            self.phone = str(phone)
            if len(mail) != 0:
                self.mail = mail
            else:
                self.mail = ''.join(choice(ascii_lowercase) for i in range(randint(10,20)))+"@gmail.com"
    
        def randomize(self):
            # Update user details
            self.f_ad = self.fake.first_name().replace("'", "").replace('"', "")
            self.f_soyad = self.fake.last_name().replace("'", "").replace('"', "")
            # Password with letters (upper and lower), numbers, no special chars that might break json, but some services require 1 uppercase, 1 lowercase, 1 number
            self.f_sifre = self.fake.password(length=8, special_chars=False, upper_case=True, lower_case=True) + "1a*"
            # Update session & stealth details (new headers, proxies, UA, etc.)
            self.headers_pool, self.proxies, self.session, self.engine = stealth_ayarla(self.stealth_config)
    '''
    text = re.sub(__init__pattern, init_replacement, text, flags=re.DOTALL, count=1)
    
    
    # Inject `self.randomize()` into every service function
    # Service functions are def Name(self): ...
    def inject_randomize(match):
        name = match.group(1)
        # Exclude __init__ and randomize
        if name in ["__init__", "randomize"]:
            return match.group(0)
        body = match.group(2)
        # Insert self.randomize() right after try:
        body = re.sub(r'(\s+)try:', r'\1try:\1    self.randomize()', body, count=1)
        
        # Replace static values
        body = re.sub(r'["\']Memati["\']', "self.f_ad", body)
        body = re.sub(r'["\']Bas["\']', "self.f_soyad", body)
        body = re.sub(r'["\']MEMAT[Iİ]["\']', "self.f_ad.upper()", body)
        body = re.sub(r'["\']BAS["\']', "self.f_soyad.upper()", body)
        body = re.sub(r'["\']Memati Bas["\']', "f\"{self.f_ad} {self.f_soyad}\"", body)
    
        for pw in ['"31ABC..abc31"', '"313131"', '"123456"', '"31MeMaTi31"', '"Memati31"']:
            body = body.replace(pw, "self.f_sifre")
            
        body = re.sub(r'["\']User-Agent["\']\s*:\s*["\'].*?["\'],?\s*', '', body)
    
        return f"def {name}(self):" + body
    
    
    text = re.sub(r'def ([a-zA-Z0-9_]+)\(self\):(.*?)(?=\n    def |\Z)', inject_randomize, text, flags=re.DOTALL)
    
    with open("moduls/sms/services.py", "w", encoding="utf-8") as f:
        f.write(text)
    
    print("Updated moduls/sms/services.py")