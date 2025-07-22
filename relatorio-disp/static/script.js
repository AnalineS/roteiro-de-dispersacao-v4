class ChatbotInterface {
    constructor() {
        this.chatWindow = document.getElementById('chat-window');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        this.personaToggle = document.getElementById('persona-toggle');
        this.personaLabel = document.getElementById('persona-label');
        this.errorContainer = document.getElementById('error-container');
        this.statusText = document.getElementById('status-text');
        this.mainAvatarProfessor = document.getElementById('avatar-professor');
        this.mainAvatarAmigo = document.getElementById('avatar-amigo');
        
        this.currentPersona = 'professor';
        this.isProcessing = false;
        this.chatHistory = [];

        this.personas = {
            professor: {
                name: 'Dr. Gasnelio',
                avatar: 'https://i.postimg.cc/NfdHCVM7/Chat-GPT-Image-13-de-jul-de-2025-00-09-29.png',
                welcome: 'Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica. Como posso auxiliá-lo hoje?',
                prompt: 'Você é o Dr. Gasnelio, um farmacêutico especialista e pesquisador. Responda de forma técnica, precisa e educada, como um professor universitário. Sua base de conhecimento é uma tese sobre roteiros de dispensação para hanseníase.'
            },
            amigo: {
                name: 'Gá',
                avatar: 'https://i.postimg.cc/j5YwJYgK/Chat-GPT-Image-13-de-jul-de-2025-00-14-18.png',
                welcome: 'Opa, tudo certo? Aqui é o Gá! Tô aqui pra gente desenrolar qualquer dúvida sobre o uso correto de medicamentos e o roteiro de dispensação. Manda a ver!',
                prompt: 'Você é o Gá, um farmacêutico amigável e profissional. Responda de forma casual, simples e encorajadora, como um amigo. Sua base de conhecimento é uma tese sobre roteiros de dispensação para hanseníase.'
            }
        };
        
        this.init();
    }
    
    init() {
        if (!this.chatWindow) return;
        this.chatWindow.innerHTML = '';
        this.loadPersona();
        this.setupEventListeners();
        this.setupPersonaToggle();
        this.addMessage(this.personas[this.currentPersona].welcome, 'bot');
    }

    loadPersona() {
        const savedPersona = localStorage.getItem('teseWebPersona');
        if (savedPersona && (savedPersona === 'professor' || savedPersona === 'amigo')) {
            this.currentPersona = savedPersona;
        }
        if (this.currentPersona === 'amigo') {
            this.personaToggle.classList.add('active');
        } else {
            this.personaToggle.classList.remove('active');
        }
        this.personaLabel.textContent = this.currentPersona.charAt(0).toUpperCase() + this.currentPersona.slice(1);
        this.updateMainAvatar();
    }
    
    setupEventListeners() {
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.chatInput.addEventListener('keypress', (e) => this.handleKeyPress(e));
    }
    
    setupPersonaToggle() {
        this.personaToggle.addEventListener('click', () => {
            this.personaToggle.classList.toggle('active');
            this.currentPersona = this.personaToggle.classList.contains('active') ? 'amigo' : 'professor';
            localStorage.setItem('teseWebPersona', this.currentPersona);
            this.personaLabel.textContent = this.currentPersona.charAt(0).toUpperCase() + this.currentPersona.slice(1);
            this.updateMainAvatar();

            this.chatWindow.innerHTML = '';
            this.chatHistory = [];
            const welcomeMessage = this.personas[this.currentPersona].welcome;
            this.addMessage(welcomeMessage, 'bot');
        });
    }

    updateMainAvatar() {
        if (this.currentPersona === 'professor') {
            this.mainAvatarProfessor.classList.remove('hidden');
            this.mainAvatarAmigo.classList.add('hidden');
        } else {
            this.mainAvatarProfessor.classList.add('hidden');
            this.mainAvatarAmigo.classList.remove('hidden');
        }
    }

    handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.handleSubmit(e);
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        if (this.isProcessing) return;
        
        const message = this.chatInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        await this.processBotResponse(message);
        this.chatInput.value = '';
        this.chatInput.focus();
    }
    
    async processBotResponse(message) {
        this.isProcessing = true;
        this.updateUIState(true);
        this.showTypingIndicator();
        
        try {
            const responseText = await this.fetchLLMResponse(message);
            this.hideTypingIndicator();
            const md = window.markdownit();
            this.addMessage(md.render(responseText), 'bot');
        } catch (error) {
            this.hideTypingIndicator();
            this.showError('Desculpe, ocorreu um erro ao conectar. Tente novamente.');
            console.error('Chatbot Error:', error);
        } finally {
            this.isProcessing = false;
            this.updateUIState(false);
        }
    }

    async fetchLLMResponse(userMessage) {
        // Configuração da API com melhorias implementadas
        const apiUrl = '/api/chat';
        const personality_id = this.currentPersona === 'professor' ? 'dr_gasnelio' : 'ga';
        
        const payload = {
            question: userMessage,
            personality_id: personality_id
        };

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`API error: ${response.status} ${response.statusText} - ${errorData}`);
            }

            const result = await response.json();
            
            if (result.answer) {
                // Adiciona ao histórico
                this.chatHistory.push({ role: "user", parts: [{ text: userMessage }] });
                this.chatHistory.push({ role: "model", parts: [{ text: result.answer }] });
                
                // Log das melhorias para debug
                console.log('Resposta com melhorias:', {
                    answer: result.answer,
                    confidence: result.confidence,
                    source: result.source,
                    personality: result.personality
                });
                
                return result.answer;
            } else {
                console.error("Resposta da API sem resposta:", result);
                return "Desculpe, não consegui processar sua pergunta. Tente novamente.";
            }
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }
    
    addMessage(text, sender) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `w-full flex gap-3 items-end ${sender === 'user' ? 'justify-end' : 'justify-start'} message-slide-in`;
        const messageBubble = document.createElement('div');
        messageBubble.className = `message-bubble max-w-md lg:max-w-lg p-3 rounded-2xl shadow-lg`;
        
        if (sender === 'user') {
            messageBubble.classList.add('bg-primary-color', 'text-white', 'rounded-br-lg');
            const p = document.createElement('p');
            p.textContent = text;
            messageBubble.appendChild(p);
            messageContainer.appendChild(messageBubble);
        } else {
            messageBubble.classList.add('bg-white/90', 'text-slate-800', 'rounded-bl-lg');
            messageBubble.innerHTML = text;
            const avatar = document.createElement('img');
            avatar.className = 'w-8 h-8 rounded-full object-cover flex-shrink-0';
            const personaData = this.personas[this.currentPersona];
            avatar.src = personaData.avatar;
            avatar.alt = personaData.name;
            avatar.style.objectFit = 'cover';
            avatar.loading = 'lazy';
            messageContainer.appendChild(avatar);
            messageContainer.appendChild(messageBubble);
        }
        
        this.chatWindow.appendChild(messageContainer);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const indicatorContainer = document.createElement('div');
        indicatorContainer.id = 'typing-indicator';
        indicatorContainer.className = 'w-full flex gap-3 items-end justify-start message-slide-in';
        const personaData = this.personas[this.currentPersona];
        indicatorContainer.innerHTML = `
            <img src="${personaData.avatar}" alt="${personaData.name}" class="w-8 h-8 rounded-full object-cover flex-shrink-0" style="object-fit: cover;" loading="lazy">
            <div class="message-bubble bg-white/90 rounded-2xl rounded-bl-lg shadow-lg">
                <div class="typing-indicator">
                    <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
                </div>
            </div>`;
        this.chatWindow.appendChild(indicatorContainer);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }
    
    updateUIState(processing) {
        this.sendButton.disabled = processing;
        this.chatInput.disabled = processing;
        
        if (processing) {
            this.sendButton.innerHTML = `<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>`;
            this.statusText.textContent = 'Processando...';
        } else {
            this.sendButton.innerHTML = `<i data-lucide="send-horizontal"></i>`;
            lucide.createIcons();
            this.statusText.textContent = 'Online';
        }
    }
    
    showError(message) {
        this.errorContainer.innerHTML = `<div class="bg-red-500/90 backdrop-blur-sm text-white p-3 rounded-lg border border-red-400 text-center text-sm">${message}</div>`;
        setTimeout(() => { this.errorContainer.innerHTML = ''; }, 5000);
    }
    
    scrollToBottom() {
        setTimeout(() => { this.chatWindow.scrollTop = this.chatWindow.scrollHeight; }, 50);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    const hamburgerButton = document.getElementById('hamburger-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if(hamburgerButton && mobileMenu) {
        hamburgerButton.addEventListener('click', () => {
            hamburgerButton.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }

    const navLinks = document.querySelectorAll('.nav-link');
    const pageSections = document.querySelectorAll('.page-section');
    function updateActiveLink() {
        let currentSection = '';
        pageSections.forEach(section => {
            if (window.scrollY >= section.offsetTop - 80) {
                currentSection = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') && link.getAttribute('href').includes(currentSection)) {
                link.classList.add('active');
            }
        });
    }
    if (pageSections.length > 0) {
        window.addEventListener('scroll', updateActiveLink);
        updateActiveLink();
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const submitButton = document.getElementById('contact-submit-button');
            const originalButtonContent = submitButton.innerHTML;
            
            submitButton.disabled = true;
            submitButton.innerHTML = `<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>`;

            setTimeout(() => {
                const formSuccessMessage = document.getElementById('form-success');
                formSuccessMessage.classList.remove('hidden');
                contactForm.reset();
                
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonContent;
                lucide.createIcons();

                setTimeout(() => {
                    formSuccessMessage.classList.add('hidden');
                }, 5000);
            }, 1000);
        });
    }
    
    if (document.getElementById('chatbot')) {
        new ChatbotInterface();
    }
});
