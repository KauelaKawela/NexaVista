import re

with open("NexaVista.py", "r", encoding="utf-8") as f:
    code = f.read()

# Remove 'js' from export formats prompt
code = code.replace("[md,txt,html,xml,js]", "[md,txt,html,xml]")

# Menu Updates
code = re.sub(
    r'\{clr\.am4\}║ 2 - Gecersiz Link Tespiti           ║\n'
    r'\{clr\.am5\}║ 3 - Linklerden Baslik Cek           ║',
    f'{{clr.am4}}║ 2 - SMS Bomber                      ║\n'
    f'{{clr.am5}}║ 3 - DDoS Saldırı                    ║',
    code
)

# Update secim_haritasi
code = code.replace(
    '''        "1": standart_tarama,\n        "2": gecersiz_tarama,\n        "3": ctl.baslık_cek,''',
    '''        "1": standart_tarama,\n        "2": call_sms_bomber,\n        "3": call_ddos_attack,'''
)

# Insert the functions
insert_funcs = '''
def call_sms_bomber():
    from modules.sms.sms_bomber import run_sms
    run_sms()

def call_ddos_attack():
    from modules.ddos.ddos_attack import run_ddos
    run_ddos()
'''
code = code.replace("def MENU(secilmis):", insert_funcs + "\ndef MENU(secilmis):")

with open("NexaVista.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Updated NexaVista.py")
