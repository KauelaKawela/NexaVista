if __name__ == "__main__":
    import re
    
    with open("moduls/sms/services.py", "r", encoding="utf-8") as f:
        code = f.read()
    
    
    if "from core.stealth import StealthConfig, stealth_ayarla, STEALTH_FULL" not in code:
        code = code.replace("import requests", "import requests\nfrom core.stealth import StealthConfig, stealth_ayarla, STEALTH_FULL\n")
    
    init_pattern = r'(def __init__\(self, phone, mail\):)'
    new_init = '''def __init__(self, phone, mail):
            self.stealth_config = StealthConfig.from_level(STEALTH_FULL)
            self.headers_pool, self.proxies, self.session, self.engine = stealth_ayarla(self.stealth_config)
    '''
    code = re.sub(init_pattern, new_init, code)
    
    code = re.sub(r'requests\.post\(([^)]*)\)', r'self.session.post(\1, proxies=self.proxies)', code)
    code = code.replace("proxies=self.proxies, proxies=self.proxies", "proxies=self.proxies")
    
    with open("moduls/sms/services.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("Updated services.py")