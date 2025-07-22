#!/usr/bin/env python3
"""
Script para adicionar novas doenças ao chatbot multi-doenças
"""

import json
import os
import re

def add_new_disease():
    """Interface para adicionar nova doença"""
    print("=" * 50)
    print("    ADICIONAR NOVA DOENÇA AO CHATBOT")
    print("=" * 50)
    print()
    
    # Coletar informações da doença
    disease_id = input("ID da doença (ex: cancer, tuberculose): ").strip().lower()
    disease_name = input("Nome da doença (ex: Câncer, Tuberculose): ").strip()
    description = input("Descrição da doença: ").strip()
    keywords = input("Palavras-chave (separadas por vírgula): ").strip()
    
    # Verificar se PDF existe
    pdf_path = f"PDFs/{disease_id}.pdf"
    pdf_exists = os.path.exists(pdf_path)
    
    if not pdf_exists:
        print(f"\n⚠️  AVISO: PDF não encontrado em {pdf_path}")
        print("O chatbot funcionará apenas com respostas padrão para esta doença")
    
    # Personalidades padrão
    personalities = {
        "dr_gasnelio": {
            "name": "Dr. Gasnelio",
            "style": "sério e técnico",
            "greeting": f"Olá! Sou o Dr. Gasnelio, especialista em {disease_name.lower()}. Como posso ajudá-lo hoje?",
            "fallback": f"Baseado na literatura médica sobre {disease_name.lower()}, posso orientar que esta condição requer avaliação médica especializada. Recomendo consultar um médico para diagnóstico adequado."
        },
        "ga": {
            "name": "Gá",
            "style": "descontraído e simples",
            "greeting": f"Oi! Sou o Gá! 😊 Vou te ajudar a entender sobre {disease_name.lower()} de um jeito bem simples!",
            "fallback": f"Olha, sobre isso eu não tenho certeza no material que tenho aqui. Mas posso te dizer que é sempre bom procurar um médico quando temos dúvidas sobre saúde, certo? 😊"
        }
    }
    
    # Criar estrutura da doença
    new_disease = {
        "name": disease_name,
        "pdf_path": pdf_path,
        "description": description,
        "keywords": [kw.strip() for kw in keywords.split(",")],
        "personalities": personalities
    }
    
    # Mostrar resumo
    print("\n" + "=" * 50)
    print("    RESUMO DA NOVA DOENÇA")
    print("=" * 50)
    print(f"ID: {disease_id}")
    print(f"Nome: {disease_name}")
    print(f"Descrição: {description}")
    print(f"Palavras-chave: {', '.join(new_disease['keywords'])}")
    print(f"PDF: {pdf_path} {'✅' if pdf_exists else '❌'}")
    print(f"Personalidades: Dr. Gasnelio, Gá")
    
    # Confirmar
    confirm = input("\nConfirma a adição desta doença? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operação cancelada.")
        return
    
    # Gerar código Python
    python_code = generate_python_code(disease_id, new_disease)
    
    # Salvar em arquivo
    filename = f"disease_{disease_id}.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"\n✅ Código gerado em: {filename}")
    print("\nPara adicionar ao sistema:")
    print("1. Abra o arquivo app_multi_disease.py")
    print("2. Localize a seção 'diseases'")
    print("3. Adicione o código gerado")
    print("4. Reinicie o servidor")
    
    # Mostrar código
    print(f"\n{'='*50}")
    print("    CÓDIGO PARA ADICIONAR AO app_multi_disease.py")
    print("="*50)
    print(python_code)

def generate_python_code(disease_id, disease_data):
    """Gera código Python para adicionar a doença"""
    code = f'''                "{disease_id}": {{
                    "name": "{disease_data['name']}",
                    "pdf_path": "{disease_data['pdf_path']}",
                    "description": "{disease_data['description']}",
                    "keywords": {json.dumps(disease_data['keywords'], ensure_ascii=False)},
                    "personalities": {{
                        "dr_gasnelio": {{
                            "name": "Dr. Gasnelio",
                            "style": "sério e técnico",
                            "greeting": "{disease_data['personalities']['dr_gasnelio']['greeting']}",
                            "fallback": "{disease_data['personalities']['dr_gasnelio']['fallback']}"
                        }},
                        "ga": {{
                            "name": "Gá",
                            "style": "descontraído e simples",
                            "greeting": "{disease_data['personalities']['ga']['greeting']}",
                            "fallback": "{disease_data['personalities']['ga']['fallback']}"
                        }}
                    }}
                }},'''
    return code

def list_existing_diseases():
    """Lista doenças já configuradas"""
    print("=" * 50)
    print("    DOENÇAS JÁ CONFIGURADAS")
    print("=" * 50)
    
    # Ler app_multi_disease.py para extrair doenças
    try:
        with open('app_multi_disease.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair doenças usando regex
        disease_pattern = r'"([^"]+)":\s*{\s*"name":\s*"([^"]+)"'
        diseases = re.findall(disease_pattern, content)
        
        for disease_id, disease_name in diseases:
            pdf_path = f"PDFs/{disease_id}.pdf"
            pdf_exists = os.path.exists(pdf_path)
            status = "✅" if pdf_exists else "❌"
            print(f"{disease_id}: {disease_name} {status}")
            
    except FileNotFoundError:
        print("Arquivo app_multi_disease.py não encontrado")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

def main():
    """Menu principal"""
    while True:
        print("\n" + "=" * 50)
        print("    GERENCIADOR DE DOENÇAS")
        print("=" * 50)
        print("1. Listar doenças existentes")
        print("2. Adicionar nova doença")
        print("3. Sair")
        print()
        
        choice = input("Escolha uma opção (1-3): ").strip()
        
        if choice == '1':
            list_existing_diseases()
        elif choice == '2':
            add_new_disease()
        elif choice == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main() 