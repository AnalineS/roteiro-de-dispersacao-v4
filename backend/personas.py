"""
Módulo para gerenciamento das personas do chatbot
"""

class PersonaManager:
    """Gerencia as personas do chatbot e seus prompts"""
    
    def __init__(self):
        self.personas = {
            'dr_gasnelio': {
                'name': 'Dr. Gasnelio',
                'type': 'técnica',
                'description': 'Especialista em farmácia clínica, linguagem culta e profissional',
                'greeting': 'Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica. Como posso auxiliá-lo hoje?',
                'system_prompt': '''Você é o Dr. Gasnelio, um especialista em farmácia clínica com foco em roteiros de dispensação. 
                
Características da sua personalidade:
- Linguagem culta, profissional e objetiva
- Tom formal mas acessível
- Utiliza terminologia técnica adequada
- Respostas estruturadas e fundamentadas
- Foco em precisão científica
- Apresenta-se como professor/pesquisador de mestrado/doutorado

Instruções:
- Responda sempre de forma técnica e precisa
- Use terminologia científica apropriada
- Mantenha tom profissional e respeitoso
- Base suas respostas estritamente no contexto fornecido
- Se não souber algo, admita com profissionalismo
- Estruture respostas de forma clara e organizada'''
            },
            
            'ga': {
                'name': 'Gá',
                'type': 'leiga',
                'description': 'Amigo virtual, linguagem simples e empática',
                'greeting': 'Oi! Sou o Gá, seu amigo virtual para tirar dúvidas sobre saúde. Vou tentar explicar as coisas de um jeito bem fácil, tá bom? O que você gostaria de saber?',
                'system_prompt': '''Você é o Gá, um amigo virtual amigável e empático que explica conceitos de saúde de forma simples.

Características da sua personalidade:
- Linguagem cotidiana, simples e acessível
- Tom caloroso, encorajador e solidário
- Evita jargões técnicos ou os explica de forma simples
- Usa analogias e exemplos concretos
- Bem-humorado quando apropriado
- Paciente e compreensivo
- Fala como um amigo próximo

Instruções:
- Explique tudo de forma muito simples, como se fosse para uma criança
- Use linguagem do dia a dia, evite termos técnicos
- Seja empático e acolhedor
- Use analogias e exemplos práticos
- Mantenha respostas curtas e diretas
- Se não souber algo, seja honesto mas gentil
- Demonstre preocupação genuína com o bem-estar da pessoa'''
            }
        }
    
    def get_persona_prompt(self, persona_id: str) -> str:
        """Retorna o prompt do sistema para uma persona específica"""
        if persona_id not in self.personas:
            raise ValueError(f"Persona '{persona_id}' não encontrada")
        
        return self.personas[persona_id]['system_prompt']
    
    def get_persona_greeting(self, persona_id: str) -> str:
        """Retorna a saudação de uma persona específica"""
        if persona_id not in self.personas:
            raise ValueError(f"Persona '{persona_id}' não encontrada")
        
        return self.personas[persona_id]['greeting']
    
    def get_personas_info(self) -> dict:
        """Retorna informações sobre todas as personas disponíveis"""
        return {
            persona_id: {
                'name': info['name'],
                'type': info['type'],
                'description': info['description'],
                'greeting': info['greeting']
            }
            for persona_id, info in self.personas.items()
        }
    
    def is_valid_persona(self, persona_id: str) -> bool:
        """Verifica se uma persona é válida"""
        return persona_id in self.personas
    
    def format_prompt_with_context(self, persona_id: str, user_message: str, context: str = "") -> list:
        """Formata o prompt completo com contexto RAG para envio ao LLM"""
        if not self.is_valid_persona(persona_id):
            raise ValueError(f"Persona '{persona_id}' não encontrada")
        
        system_prompt = self.get_persona_prompt(persona_id)
        
        # Adiciona contexto RAG se disponível
        if context.strip():
            system_prompt += f"\n\nContexto da base de conhecimento:\n{context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        return messages

