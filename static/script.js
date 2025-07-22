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
        this.loadHistory(); // NOVO: carrega histórico salvo
        this.setupEventListeners();
        this.setupPersonaToggle();
        if (this.chatHistory.length === 0) {
            this.addMessage(this.personas[this.currentPersona].welcome, 'bot');
        } else {
            this.renderHistory(); // NOVO: renderiza histórico salvo
        }
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

    loadHistory() {
        const saved = localStorage.getItem('teseWebChatHistory_' + this.currentPersona);
        try {
            this.chatHistory = saved ? JSON.parse(saved) : [];
        } catch (e) {
            this.chatHistory = [];
            localStorage.removeItem('teseWebChatHistory_' + this.currentPersona);
        }
    }

    saveHistory() {
        // Limita o histórico a 30 mensagens para evitar travamentos
        if (this.chatHistory.length > 30) {
            this.chatHistory = this.chatHistory.slice(this.chatHistory.length - 30);
        }
        localStorage.setItem('teseWebChatHistory_' + this.currentPersona, JSON.stringify(this.chatHistory));
    }

    renderHistory() {
        this.chatWindow.innerHTML = '';
        for (const msg of this.chatHistory) {
            // Se a mensagem tem informações de persona, usa elas
            if (msg.persona && msg.persona !== this.currentPersona) {
                // Se a persona mudou, não renderiza mensagens de outras personas
                continue;
            }
            this.addMessage(msg.text, msg.sender, msg.meta);
        }
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
            this.loadHistory(); // NOVO: carrega histórico ao trocar persona
            if (this.chatHistory.length === 0) {
                this.chatWindow.innerHTML = '';
                const welcomeMessage = this.personas[this.currentPersona].welcome;
                this.addMessage(welcomeMessage, 'bot');
            } else {
                this.renderHistory();
            }
        });
    }

    updateMainAvatar() {
        if (this.currentPersona === 'professor') {
            this.mainAvatarProfessor.classList.remove('hidden');
            this.mainAvatarAmigo.classList.add('hidden');
            // Atualiza o título para Dr. Gasnelio
            const titleElement = document.querySelector('h3.text-xl.font-bold.text-secondary-color');
            if (titleElement) {
                titleElement.textContent = 'Dr. Gasnelio';
            }
        } else {
            this.mainAvatarProfessor.classList.add('hidden');
            this.mainAvatarAmigo.classList.remove('hidden');
            // Atualiza o título para Gá
            const titleElement = document.querySelector('h3.text-xl.font-bold.text-secondary-color');
            if (titleElement) {
                titleElement.textContent = 'Gá';
            }
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
            const responseObj = await this.fetchLLMResponse(message);
            this.hideTypingIndicator();
            // Processa o texto sem markdownit para evitar erros
            const processedText = this.processText(responseObj.answer || responseObj);
            // Passa meta (confidence, source, personality)
            if (!responseObj.answer || responseObj.answer.trim() === '' || responseObj.source === 'no_answer') {
                this.addMessage('Nenhuma resposta encontrada para sua pergunta. Tente reformular ou perguntar de outra forma.', 'bot', {
                    confidence: 0,
                    source: responseObj.source
                });
            } else {
                this.addMessage(processedText, 'bot', {
                    confidence: responseObj.confidence,
                    source: responseObj.source,
                    personality: responseObj.personality
                });
            }
        } catch (error) {
            this.hideTypingIndicator();
            // Diferencia tipos de erro
            let msg = '';
            if (error.message && error.message.includes('Failed to fetch')) {
                msg = 'Erro de conexão com o servidor. Verifique sua internet ou tente novamente mais tarde.';
            } else if (error.message && error.message.includes('API error')) {
                msg = 'Erro interno do servidor. Tente novamente em alguns minutos.';
            } else {
                msg = 'Erro inesperado. Tente recarregar a página ou reformular sua pergunta.';
            }
            this.showError(msg + ' Se o problema persistir, entre em contato com o doutorando Nélio Gomes.');
            this.addMessage('Desculpe, não consegui processar sua pergunta devido a um erro técnico.', 'bot', {confidence: 0, source: 'erro'});
            console.error('Chatbot Error:', error);
        } finally {
            this.isProcessing = false;
            this.updateUIState(false);
        }
    }

    async fetchLLMResponse(userMessage) {
        // Configuração da API para Render
        const apiUrl = '/api/chat';
        const persona = this.currentPersona === 'professor' ? 'dr_gasnelio' : 'ga';
        
        const payload = {
            question: userMessage,
            personality_id: persona
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
                // Log das melhorias para debug
                console.log('Resposta com melhorias:', {
                    answer: result.answer,
                    confidence: result.confidence,
                    source: result.source,
                    personality: result.personality
                });
                
                return result;
            } else {
                console.error("Resposta da API sem resposta:", result);
                return "Desculpe, não consegui processar sua pergunta. Tente novamente.";
            }
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }
    
    addMessage(text, sender, meta = {}) {
        const messageContainer = document.createElement('div');
        // Adiciona animação de entrada (fade/slide-in)
        messageContainer.className = `w-full flex gap-3 items-end ${sender === 'user' ? 'justify-end' : 'justify-start'} message-slide-in animate-fade-in`;
        const messageBubble = document.createElement('div');
        messageBubble.className = `message-bubble max-w-md lg:max-w-lg p-3 rounded-2xl shadow-lg`;
        messageBubble.innerHTML = this.processText(text);
        if (sender === 'user') {
            messageBubble.classList.add('bg-primary-color', 'text-black', 'rounded-br-lg'); // Alterado de 'text-white' para 'text-black'
            messageContainer.appendChild(messageBubble);
        } else {
            messageBubble.classList.add('bg-white/90', 'text-slate-800', 'rounded-bl-lg');
            const avatar = document.createElement('img');
            avatar.className = 'w-8 h-8 rounded-full object-cover flex-shrink-0';
            const personaData = this.personas[this.currentPersona];
            avatar.src = personaData.avatar;
            avatar.alt = personaData.name;
            avatar.style.objectFit = 'cover';
            avatar.loading = 'lazy';
            messageContainer.appendChild(avatar);
            messageContainer.appendChild(messageBubble);
            // Adiciona rodapé de confiança/fonte se houver meta
            if (meta && (meta.confidence !== undefined || meta.source)) {
                const metaDiv = document.createElement('div');
                metaDiv.className = 'text-xs text-gray-500 mt-1 flex gap-2 items-center';
                if (meta.confidence !== undefined) {
                    const conf = Math.round(meta.confidence * 100);
                    metaDiv.innerHTML += `<span title='Confiança do modelo'>Confiança: <strong>${conf}%</strong></span>`;
                }
                if (meta.source) {
                    let fonte = meta.source;
                    let fonteLabel = fonte;
                    let fonteIcon = '';
                    if (fonte === 'pdf') { fonteLabel = 'PDF da tese'; }
                    else if (fonte === 'llm') { fonteLabel = 'Modelo LLM'; }
                    else if (fonte === 'fallback') { fonteLabel = 'Fallback'; }
                    else if (fonte === 'hibrida' || fonte === 'busca_hibrida' || fonte === 'busca híbrida' || fonte === 'busca-hibrida') {
                        fonteLabel = 'Busca híbrida';
                        fonteIcon = `<svg xmlns='http://www.w3.org/2000/svg' class='inline w-4 h-4 text-primary-color -mt-0.5 mr-1' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' /></svg>`;
                    }
                    metaDiv.innerHTML += `<span title='Fonte da resposta'>${fonteIcon}<strong>${fonteLabel}</strong></span>`;
                }
                messageBubble.appendChild(metaDiv);
            }
        }
        this.chatWindow.appendChild(messageContainer);
        
        // Salva no histórico visual com informações da persona
        const messageData = { 
            text, 
            sender,
            persona: this.currentPersona,
            timestamp: new Date().toISOString(),
            meta
        };
        this.chatHistory.push(messageData);
        this.saveHistory();
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const indicatorContainer = document.createElement('div');
        indicatorContainer.id = 'typing-indicator';
        indicatorContainer.className = 'w-full flex gap-3 items-end justify-start message-slide-in animate-fade-in';
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
            this.sendButton.innerHTML = `<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin animate-pulse"></div>`;
            this.sendButton.classList.add('animate-pulse');
            this.statusText.textContent = 'Aguardando resposta...';
        } else {
            this.sendButton.innerHTML = `<i data-lucide="send-horizontal"></i>`;
            this.sendButton.classList.remove('animate-pulse');
            lucide.createIcons();
            this.statusText.textContent = 'Online';
        }
    }
    
    showError(message) {
        this.errorContainer.innerHTML = `<div class="bg-red-500/90 backdrop-blur-sm text-white p-3 rounded-lg border border-red-400 text-center text-sm">${message}</div>`;
        setTimeout(() => { this.errorContainer.innerHTML = ''; }, 5000);
    }
    
    processText(text) {
        return text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }
    
    scrollToBottom() {
        setTimeout(() => { this.chatWindow.scrollTop = this.chatWindow.scrollHeight; }, 50);
    }
}

// Função utilitária para gerar texto simples do histórico
function getChatHistoryText(chatHistory) {
    return chatHistory.map(msg => {
        const sender = msg.sender === 'user' ? 'Você' : (msg.persona === 'professor' ? 'Dr. Gasnelio' : 'Gá');
        return `${sender}: ${msg.text.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()}`;
    }).join('\n\n');
}

// Função para exportar PDF usando jsPDF
function exportChatAsPDF(chatHistory) {
    if (typeof window.jspdf === 'undefined') {
        alert('jsPDF não carregado.');
        return;
    }
    const doc = new window.jspdf.jsPDF();
    doc.setFont('helvetica');
    doc.setFontSize(12);
    const lines = doc.splitTextToSize(getChatHistoryText(chatHistory), 180);
    doc.text(lines, 15, 20);
    doc.save('chat_historico.pdf');
}

// Função para exportar DOCX usando PizZip + docxtemplater
function exportChatAsDOCX(chatHistory) {
    if (typeof window.PizZip === 'undefined' || typeof window.docxtemplater === 'undefined') {
        alert('docxtemplater/PizZip não carregados.');
        return;
    }
    // Cria um documento simples
    const zip = new window.PizZip();
    const content = getChatHistoryText(chatHistory);
    // Modelo DOCX básico (texto simples)
    const doc = new window.docxtemplater(new window.PizZip(), { paragraphLoop: true, linebreaks: true });
    doc.loadZip(zip);
    doc.setData({ chat: content });
    try {
        doc.render();
    } catch (error) {
        alert('Erro ao gerar DOCX: ' + error.message);
        return;
    }
    const out = doc.getZip().generate({ type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
    saveAs(out, 'chat_historico.docx');
}

// Adiciona listeners para exportação
function setupExportChat(chatbotInstance) {
    const exportBtn = document.getElementById('export-chat-btn');
    const exportMenu = document.getElementById('export-menu');
    if (!exportBtn || !exportMenu) return;
    exportBtn.addEventListener('click', (e) => {
        e.preventDefault();
        exportMenu.classList.toggle('hidden');
    });
    document.addEventListener('click', (e) => {
        if (!exportBtn.contains(e.target) && !exportMenu.contains(e.target)) {
            exportMenu.classList.add('hidden');
        }
    });
    exportMenu.querySelectorAll('.export-option').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const format = btn.getAttribute('data-format');
            exportMenu.classList.add('hidden');
            const chatHistory = chatbotInstance ? chatbotInstance.chatHistory : [];
            if (format === 'pdf') {
                exportChatAsPDF(chatHistory);
            } else if (format === 'docx') {
                exportChatAsDOCX(chatHistory);
            }
        });
    });
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
        const chatbot = new ChatbotInterface();
        // Quick Prompts: perguntas rápidas
        const quickPrompts = document.getElementById('quick-prompts');
        if (quickPrompts) {
            quickPrompts.querySelectorAll('button[data-prompt]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const prompt = btn.getAttribute('data-prompt');
                    const chatInput = document.getElementById('chat-input');
                    if (chatInput) {
                        chatInput.value = prompt;
                        // dispara o envio do formulário
                        document.getElementById('chat-form').dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
                    }
                });
            });
        }
        // Exportação do chat
        setupExportChat(chatbot);
    }

    // Dark mode toggle
    const darkToggle = document.getElementById('dark-mode-toggle');
    if (darkToggle) {
        darkToggle.addEventListener('click', () => {
            const html = document.documentElement;
            const isDark = html.classList.toggle('dark');
            localStorage.setItem('darkMode', isDark ? 'true' : 'false');
            // Atualiza ícones
            document.getElementById('icon-sun').style.display = isDark ? 'none' : '';
            document.getElementById('icon-moon').style.display = isDark ? '' : 'none';
        });
        // Atualiza ícones ao carregar
        const isDark = document.documentElement.classList.contains('dark');
        document.getElementById('icon-sun').style.display = isDark ? 'none' : '';
        document.getElementById('icon-moon').style.display = isDark ? '' : 'none';
    }
});

// Adiciona animação fade-in via CSS
const style = document.createElement('style');
style.innerHTML = `
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
.animate-fade-in { animation: fadeInUp 0.5s cubic-bezier(0.4,0,0.2,1); }
.animate-pulse { animation: pulse 1.2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
`;
document.head.appendChild(style);
