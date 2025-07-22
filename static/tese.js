// Script específico para a página da tese
document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade das abas de doenças
    const tabHansen = document.getElementById('tab-hansen');
    const tabFake = document.getElementById('tab-fake');
    const contentHansen = document.getElementById('content-hansen');
    const contentFake = document.getElementById('content-fake');
    const sidebarHansen = document.getElementById('sidebar-hansen');
    const sidebarFake = document.getElementById('sidebar-fake');

    if (tabHansen && tabFake) {
        // Função para alternar entre abas
        function switchTab(activeTab, inactiveTab, activeContent, inactiveContent, activeSidebar, inactiveSidebar) {
            // Remove classes ativas
            inactiveTab.classList.remove('active-tab');
            inactiveContent.classList.remove('hidden');
            inactiveSidebar.classList.remove('hidden');
            
            // Adiciona classes ativas
            activeTab.classList.add('active-tab');
            activeContent.classList.add('hidden');
            activeSidebar.classList.add('hidden');
        }

        // Event listeners para as abas
        tabHansen.addEventListener('click', function() {
            switchTab(tabHansen, tabFake, contentHansen, contentFake, sidebarHansen, sidebarFake);
        });

        tabFake.addEventListener('click', function() {
            switchTab(tabFake, tabHansen, contentFake, contentHansen, sidebarFake, sidebarHansen);
        });
    }

    // Navegação suave entre seções
    const sidebarLinks = document.querySelectorAll('.thesis-sidebar a');
    
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                // Remove classe ativa de todos os links
                sidebarLinks.forEach(l => l.classList.remove('active'));
                
                // Adiciona classe ativa ao link clicado
                this.classList.add('active');
                
                // Scroll suave para a seção
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Atualizar link ativo baseado no scroll
    function updateActiveSidebarLink() {
        const sections = document.querySelectorAll('.thesis-content section');
        const sidebarLinks = document.querySelectorAll('.thesis-sidebar a');
        
        let currentSection = '';
        const scrollPosition = window.scrollY + 100; // Offset para melhor detecção
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + currentSection) {
                link.classList.add('active');
            }
        });
    }

    // Adicionar listener de scroll para atualizar link ativo
    window.addEventListener('scroll', updateActiveSidebarLink);
    
    // Executar uma vez no carregamento
    updateActiveSidebarLink();

    // Funcionalidade de voltar ao topo
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i data-lucide="arrow-up"></i>';
    backToTopButton.className = 'fixed bottom-6 right-6 bg-primary-color text-white p-3 rounded-full shadow-lg hover:bg-primary-dark transition-all duration-300 opacity-0 pointer-events-none z-50';
    backToTopButton.setAttribute('aria-label', 'Voltar ao topo');
    document.body.appendChild(backToTopButton);

    // Mostrar/ocultar botão de voltar ao topo
    function toggleBackToTopButton() {
        if (window.scrollY > 300) {
            backToTopButton.classList.remove('opacity-0', 'pointer-events-none');
        } else {
            backToTopButton.classList.add('opacity-0', 'pointer-events-none');
        }
    }

    window.addEventListener('scroll', toggleBackToTopButton);

    // Funcionalidade do botão voltar ao topo
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Inicializar ícones Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Melhorar acessibilidade
    const diseaseTabs = document.querySelectorAll('.disease-tab');
    diseaseTabs.forEach(tab => {
        tab.setAttribute('role', 'tab');
        tab.setAttribute('tabindex', '0');
        
        tab.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // Adicionar indicador de carregamento para links externos
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });

    console.log('Script da tese carregado com sucesso!');
}); 