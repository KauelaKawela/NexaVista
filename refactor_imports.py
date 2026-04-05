import os

FILES = [
    "./core/clr.py",
    "./core/config.py",
    "./core/formated.py",
    "./core/helper_func.py",
    "./core/__init__.py",
    "./core/models.py",
    "./core/stealth.py",
    "./modules/ddos/ddos_attack.py",
    "./modules/ddos/__init__.py",
    "./modules/__init__.py",
    "./modules/proxy_checker/checker_v1.py",
    "./modules/proxy_checker/__init__.py",
    "./modules/proxy_checker/proxy_check.py",
    "./modules/scanner/analyzer.py",
    "./modules/scanner/analyzer_v2.py",
    "./modules/scanner/check_tittle.py",
    "./modules/scanner/csf.py",
    "./modules/scanner/docat.py",
    "./modules/scanner/extract.py",
    "./modules/scanner/__init__.py",
    "./modules/scanner/manager.py",
    "./modules/scanner/notfoundlinks.py",
    "./modules/scanner/reporter.py",
    "./modules/scanner/scanner.py",
    "./modules/scanner/urlstus.py",
    "./modules/scanner/usec.py",
    "./modules/scanner/wltf.py",
    "./modules/sms/__init__.py",
    "./modules/sms/randomize_sms.py",
    "./modules/sms/services.py",
    "./modules/sms/sms_bomber.py",
    "./modules/sms/update_sms.py",
    "./modules/sms/update_sms_script.py",
    "./NexaVista.py",
    "./scripts/update_categories.py",
    "./scripts/update_nexavista.py"
]

CORE_MODULES = [
    'config', 'models', 'stealth', 'helper_func', 'formated'
]
SCANNER_MODULES = [
    'manager', 'scanner', 'reporter', 'extract', 'urlstus', 
    'csf', 'usec', 'wltf', 'docat', 'notfoundlinks', 'check_tittle', 'analyzer'
]

def replace_imports(content):
    content = content.replace('import clr', 'from core import clr')
    content = content.replace('from clr import', 'from core.clr import')
    
    for mod in CORE_MODULES:
        content = content.replace(f'from datas.func import {mod}', f'from core import {mod}')
        content = content.replace(f'from datas.func.{mod} import', f'from core.{mod} import')
        content = content.replace(f'import datas.func.{mod}', f'import core.{mod}')
        
    for mod in SCANNER_MODULES:
        content = content.replace(f'from datas.func import {mod}', f'from modules.scanner import {mod}')
        content = content.replace(f'from datas.func.{mod} import', f'from modules.scanner.{mod} import')
        content = content.replace(f'import datas.func.{mod}', f'import modules.scanner.{mod}')

    content = content.replace('from datas.func import proxy_check', 'from modules.proxy_checker import proxy_check')
    content = content.replace('from datas.func.proxy_check import', 'from modules.proxy_checker.proxy_check import')
    
    content = content.replace('from moduls.sms', 'from modules.sms')
    content = content.replace('import moduls.sms', 'import modules.sms')

    content = content.replace('from moduls.ddos', 'from modules.ddos')
    content = content.replace('import moduls.ddos', 'import modules.ddos')
    
    content = content.replace('from moduls.proxy_checker', 'from modules.proxy_checker')
    content = content.replace('import moduls.proxy_checker', 'import modules.proxy_checker')

    content = content.replace('from moduls.link_analyzer', 'from modules.scanner')
    content = content.replace('import moduls.link_analyzer', 'import modules.scanner')

    return content

def handle_multi_imports(content):
    # NexaVista.py complex multi imports
    old_line = "from datas.func import helper_func, extract, urlstus, csf, formated, usec, wltf"
    new_line = "from core import helper_func, formated\nfrom modules.scanner import extract, urlstus, csf, usec, wltf"
    content = content.replace(old_line, new_line)
    
    old_line2 = "from datas.func import check_tittle as ctl"
    new_line2 = "from modules.scanner import check_tittle as ctl"
    content = content.replace(old_line2, new_line2)

    old_line3 = "from datas.func import notfoundlinks as nfl"
    new_line3 = "from modules.scanner import notfoundlinks as nfl"
    content = content.replace(old_line3, new_line3)

    return content

def process_all():
    print(f"Processing {len(FILES)} files...")
    for path in FILES:
        if not os.path.exists(path):
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = replace_imports(content)
            new_content = handle_multi_imports(new_content)
            
            if new_content != content:
                print(f"Updated {path}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error on {path}: {e}")
    print("Done!")

if __name__ == '__main__':
    process_all()
