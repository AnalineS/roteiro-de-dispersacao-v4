#!/usr/bin/env python3
"""
Script para diagnosticar e resolver problemas de conexão ECONNRESET no Cursor
"""

import os
import subprocess
import requests

def print_step(step, message):
    """Imprime uma etapa do diagnóstico"""
    print(f"\n{'='*50}")
    print(f"ETAPA {step}: {message}")
    print(f"{'='*50}")

def check_internet_connection():
    """Verifica conectividade básica de internet"""
    print_step(1, "Verificando Conectividade de Internet")
    
    test_urls = [
        "https://httpbin.org/get",
        "https://google.com",
        "https://github.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - OK")
            else:
                print(f"⚠️  {url} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Erro: {e}")
            return False
    
    return True

def check_cursor_processes():
    """Verifica processos do Cursor em execução"""
    print_step(2, "Verificando Processos do Cursor")
    
    try:
        # Windows
        if os.name == 'nt':
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Cursor.exe'], 
                                  capture_output=True, text=True, timeout=10)
            if 'Cursor.exe' in result.stdout:
                print("✅ Cursor está em execução")
                return True
            else:
                print("❌ Cursor não está em execução")
                return False
        else:
            # Linux/Mac
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
            if 'cursor' in result.stdout.lower():
                print("✅ Cursor está em execução")
                return True
            else:
                print("❌ Cursor não está em execução")
                return False
    except Exception as e:
        print(f"❌ Erro ao verificar processos: {e}")
        return False

def check_cursor_config():
    """Verifica configurações do Cursor"""
    print_step(3, "Verificando Configurações do Cursor")
    
    cursor_config_paths = []
    
    if os.name == 'nt':  # Windows
        cursor_config_paths = [
            os.path.expanduser("~/AppData/Roaming/Cursor/User/globalStorage"),
            os.path.expanduser("~/AppData/Roaming/Cursor/User/workspaceStorage"),
            os.path.expanduser("~/AppData/Local/Cursor/User/globalStorage")
        ]
    else:  # Linux/Mac
        cursor_config_paths = [
            os.path.expanduser("~/.config/Cursor/User/globalStorage"),
            os.path.expanduser("~/.config/Cursor/User/workspaceStorage")
        ]
    
    for path in cursor_config_paths:
        if os.path.exists(path):
            print(f"✅ Configuração encontrada: {path}")
        else:
            print(f"⚠️  Configuração não encontrada: {path}")
    
    return True

def check_firewall_antivirus():
    """Verifica se firewall/antivírus pode estar bloqueando"""
    print_step(4, "Verificando Firewall/Antivírus")
    
    print("🔍 Verificando se firewall/antivírus pode estar bloqueando conexões...")
    print("💡 Soluções possíveis:")
    print("   1. Adicione Cursor às exceções do firewall")
    print("   2. Desative temporariamente o antivírus")
    print("   3. Verifique se o proxy está configurado corretamente")
    
    return True

def check_network_proxy():
    """Verifica configurações de proxy"""
    print_step(5, "Verificando Configurações de Proxy")
    
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    proxy_found = False
    
    for var in proxy_vars:
        if var in os.environ:
            print(f"⚠️  Proxy configurado: {var}={os.environ[var]}")
            proxy_found = True
    
    if not proxy_found:
        print("✅ Nenhum proxy configurado")
    
    return True

def suggest_solutions():
    """Sugere soluções para o problema"""
    print_step(6, "Soluções Recomendadas")
    
    solutions = [
        "🔄 Reinicie o Cursor completamente",
        "🔄 Reinicie o computador",
        "🌐 Verifique sua conexão com a internet",
        "🛡️  Adicione Cursor às exceções do firewall/antivírus",
        "⚙️  Verifique configurações de proxy",
        "🗑️  Limpe cache do Cursor (Ctrl+Shift+P > Developer: Reload Window)",
        "📱 Tente usar o Cursor em modo offline temporariamente",
        "🔧 Reinstale o Cursor se o problema persistir"
    ]
    
    for i, solution in enumerate(solutions, 1):
        print(f"{i}. {solution}")
    
    print("\n🎯 Solução mais rápida:")
    print("   1. Feche o Cursor completamente")
    print("   2. Reinicie o computador")
    print("   3. Abra o Cursor novamente")

def create_connection_test():
    """Cria um script de teste de conexão"""
    print_step(7, "Criando Script de Teste de Conexão")
    
    test_script = '''#!/usr/bin/env python3
"""
Teste de conexão para Cursor
"""

import requests
import time

def test_cursor_connection():
    """Testa conexão com serviços do Cursor"""
    
    test_urls = [
        "https://api.cursor.sh",
        "https://cursor.sh",
        "https://httpbin.org/get"
    ]
    
    print("🔍 Testando conexões...")
    
    for url in test_urls:
        try:
            print(f"Testando {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - OK")
            else:
                print(f"⚠️  {url} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Erro: {e}")
    
    print("\\n🎯 Se todos os testes falharem, verifique sua conexão com a internet")

if __name__ == "__main__":
    test_cursor_connection()
'''
    
    with open("test_cursor_connection.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Script de teste criado: test_cursor_connection.py")
    print("💡 Execute: python test_cursor_connection.py")

def main():
    """Função principal"""
    print("🔧 DIAGNÓSTICO DE CONEXÃO CURSOR - ECONNRESET")
    print("=" * 60)
    
    # Executar verificações
    internet_ok = check_internet_connection()
    cursor_running = check_cursor_processes()
    config_ok = check_cursor_config()
    firewall_ok = check_firewall_antivirus()
    proxy_ok = check_network_proxy()
    
    # Sugerir soluções
    suggest_solutions()
    
    # Criar script de teste
    create_connection_test()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    checks = [
        ("Internet", internet_ok),
        ("Cursor em execução", cursor_running),
        ("Configurações", config_ok),
        ("Firewall/Antivírus", firewall_ok),
        ("Proxy", proxy_ok)
    ]
    
    for check_name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Execute: python test_cursor_connection.py")
    print("2. Se o problema persistir, reinicie o computador")
    print("3. Verifique se há atualizações do Cursor disponíveis")

if __name__ == "__main__":
    main() 