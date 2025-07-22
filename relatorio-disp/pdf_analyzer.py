#!/usr/bin/env python3
"""
Analisador de compatibilidade do PDF para o chatbot
"""

import os
import sys
import pdfplumber
import json
from typing import Dict
import re

class PDFAnalyzer:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.analysis = {}
        
    def analyze_pdf(self) -> Dict:
        """Analisa o PDF e retorna informações detalhadas"""
        print(f"🔍 Analisando PDF: {self.pdf_path}")
        
        if not os.path.exists(self.pdf_path):
            print(f"❌ Arquivo não encontrado: {self.pdf_path}")
            return {"error": "PDF não encontrado"}
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # Informações básicas
                self.analysis["total_pages"] = len(pdf.pages)
                self.analysis["file_size_mb"] = os.path.getsize(self.pdf_path) / (1024 * 1024)
                
                # Extrair texto
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        full_text += f"\n--- Página {page_num + 1} ---\n{page_text}\n"
                        page_texts.append({
                            "page": page_num + 1,
                            "text": page_text,
                            "char_count": len(page_text),
                            "word_count": len(page_text.split())
                        })
                
                self.analysis["total_characters"] = len(full_text)
                self.analysis["total_words"] = len(full_text.split())
                self.analysis["page_texts"] = page_texts
                self.analysis["full_text"] = full_text
                
                # Análise de complexidade
                self.analyze_complexity(full_text)
                
                # Análise de compatibilidade
                self.analyze_compatibility()
                
                return self.analysis
                
        except Exception as e:
            print(f"❌ Erro ao analisar PDF: {e}")
            return {"error": str(e)}
    
    def analyze_complexity(self, text: str):
        """Analisa a complexidade do texto"""
        # Estatísticas de complexidade
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        # Média de palavras por frase
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        
        # Palavras únicas
        unique_words = set(re.findall(r'\b\w+\b', text.lower()))
        
        # Termos técnicos (exemplo para área médica)
        technical_terms = [
            'hanseníase', 'lepra', 'mycobacterium', 'bacilo', 'tratamento',
            'medicamento', 'farmacêutico', 'dispensação', 'posologia',
            'dose', 'administração', 'via', 'oral', 'intramuscular',
            'rifampicina', 'dapsona', 'clofazimina', 'poliquimioterapia',
            'protocolo', 'orientação', 'adesão', 'reação', 'adversa',
            'interação', 'medicamentosa', 'contraindicação', 'precaução'
        ]
        
        found_technical_terms = [term for term in technical_terms if term in text.lower()]
        
        self.analysis["complexity"] = {
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "unique_words": len(unique_words),
            "technical_terms_found": len(found_technical_terms),
            "technical_terms": found_technical_terms,
            "text_density": len(text) / self.analysis["total_pages"] if self.analysis["total_pages"] > 0 else 0
        }
    
    def analyze_compatibility(self):
        """Analisa a compatibilidade com o modelo de IA"""
        total_chars = self.analysis["total_characters"]
        total_pages = self.analysis["total_pages"]
        
        # Limites do modelo RoBERTa
        MODEL_MAX_CONTEXT = 512  # tokens (aproximadamente 4000 caracteres)
        RECOMMENDED_CHUNK_SIZE = 2000  # caracteres
        
        # Calcular número de chunks necessários
        num_chunks = (total_chars // RECOMMENDED_CHUNK_SIZE) + 1
        
        # Análise de compatibilidade
        compatibility = {
            "model_max_context": MODEL_MAX_CONTEXT,
            "recommended_chunk_size": RECOMMENDED_CHUNK_SIZE,
            "estimated_chunks": num_chunks,
            "total_chars": total_chars,
            "total_pages": total_pages,
            "chars_per_page": total_chars / total_pages if total_pages > 0 else 0
        }
        
        # Recomendações
        recommendations = []
        
        if total_chars > 100000:  # PDF muito grande
            recommendations.append("PDF muito extenso - considere usar chunking avançado")
            recommendations.append("Implemente busca semântica para melhor performance")
            compatibility["complexity_level"] = "HIGH"
        elif total_chars > 50000:  # PDF médio
            recommendations.append("PDF de tamanho médio - chunking recomendado")
            recommendations.append("Considere cache de respostas")
            compatibility["complexity_level"] = "MEDIUM"
        else:  # PDF pequeno
            recommendations.append("PDF de tamanho adequado")
            recommendations.append("Processamento direto possível")
            compatibility["complexity_level"] = "LOW"
        
        if total_pages > 50:
            recommendations.append("Muitas páginas - implemente navegação por seções")
        
        if self.analysis["complexity"]["technical_terms_found"] > 20:
            recommendations.append("Muitos termos técnicos - otimize o dicionário de simplificação")
        
        compatibility["recommendations"] = recommendations
        self.analysis["compatibility"] = compatibility
    
    def generate_optimized_config(self) -> Dict:
        """Gera configuração otimizada baseada na análise"""
        complexity = self.analysis.get("complexity_level", "MEDIUM")
        
        config = {
            "chunk_size": 2000,
            "overlap": 200,
            "max_answer_length": 200,
            "confidence_threshold": 0.3,
            "use_semantic_search": False,
            "use_caching": False,
            "model_name": "deepset/roberta-base-squad2"
        }
        
        if complexity == "HIGH":
            config.update({
                "chunk_size": 1500,
                "overlap": 300,
                "use_semantic_search": True,
                "use_caching": True,
                "max_answer_length": 150
            })
        elif complexity == "MEDIUM":
            config.update({
                "chunk_size": 2000,
                "overlap": 200,
                "use_caching": True
            })
        
        return config
    
    def print_analysis(self):
        """Imprime a análise de forma organizada"""
        print("\n" + "="*60)
        print("📊 ANÁLISE DE COMPATIBILIDADE DO PDF")
        print("="*60)
        
        if "error" in self.analysis:
            print(f"❌ Erro: {self.analysis['error']}")
            return
        
        print(f"📄 Informações Básicas:")
        print(f"   - Páginas: {self.analysis['total_pages']}")
        print(f"   - Tamanho: {self.analysis['file_size_mb']:.2f} MB")
        print(f"   - Caracteres: {self.analysis['total_characters']:,}")
        print(f"   - Palavras: {self.analysis['total_words']:,}")
        
        print(f"\n🧠 Complexidade:")
        comp = self.analysis["complexity"]
        print(f"   - Palavras por frase: {comp['avg_words_per_sentence']}")
        print(f"   - Palavras únicas: {comp['unique_words']:,}")
        print(f"   - Termos técnicos: {comp['technical_terms_found']}")
        
        print(f"\n⚙️ Compatibilidade:")
        compat = self.analysis["compatibility"]
        print(f"   - Nível: {compat['complexity_level']}")
        print(f"   - Chunks estimados: {compat['estimated_chunks']}")
        print(f"   - Caracteres por página: {compat['chars_per_page']:.0f}")
        
        print(f"\n💡 Recomendações:")
        for rec in compat["recommendations"]:
            print(f"   - {rec}")
        
        print(f"\n🔧 Configuração Otimizada:")
        config = self.generate_optimized_config()
        for key, value in config.items():
            print(f"   - {key}: {value}")
        
        print("="*60)

def main():
    """Função principal"""
    pdf_path = "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    
    analyzer = PDFAnalyzer(pdf_path)
    analysis = analyzer.analyze_pdf()
    
    if "error" not in analysis:
        analyzer.print_analysis()
        
        # Salvar análise em JSON
        with open("pdf_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Análise salva em: pdf_analysis.json")
        
        # Gerar configuração otimizada
        config = analyzer.generate_optimized_config()
        with open("optimized_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"💾 Configuração salva em: optimized_config.json")

if __name__ == "__main__":
    main() 