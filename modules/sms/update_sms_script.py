if __name__ == "__main__":
    import re
    
    with open("moduls/sms/services.py", "r", encoding="utf-8") as f:
        text = f.read()
    
    # 1. Update the __init__ to include faker and randomize
    init_code_search = re.search(r'def __init__.*?self\.mail = .*?@gmail\.com"', text, flags=re.DOTALL)
    if init_code_search:
        original_init = init_code_search.group(0)
        
        new_init_and_randomize = original_init + """
            from faker import Faker
            self.fake = Faker("tr_TR")
            self.stealth_config = StealthConfig.from_level(STEALTH_FULL)
            self.randomize()
    
        def randomize(self):
            self.f_ad = self.fake.first_name().replace("'", "").replace('"', "")
            self.f_soyad = self.fake.last_name().replace("'", "").replace('"', "")
            self.f_sifre = self.fake.password(length=8, special_chars=False, upper_case=True, lower_case=True) + "1a*"
            self.headers_pool, self.proxies, self.session, self.engine = stealth_ayarla(self.stealth_config)
    """
    
        pass