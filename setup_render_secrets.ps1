# Script para configurar secrets do Render no GitHub
Write-Host "🚀 Configuração de Secrets para Deploy Automático Render" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path ".git")) {
    Write-Host "❌ Erro: Execute este script no diretório raiz do repositório Git" -ForegroundColor Red
    exit 1
}

# Verificar se o Git está configurado
try {
    $remoteUrl = git remote get-url origin
    Write-Host "✅ Repositório Git encontrado: $remoteUrl" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro: Repositório Git não configurado" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Secrets necessários para o deploy automático:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. RENDER_API_KEY" -ForegroundColor Cyan
Write-Host "   - Acesse: https://dashboard.render.com"
Write-Host "   - Account Settings → API Keys → Create API Key"
Write-Host "   - Copie a chave gerada (começa com 'rnd_')"
Write-Host ""

Write-Host "2. RENDER_SERVICE_ID" -ForegroundColor Cyan
Write-Host "   - Acesse seu serviço no Render"
Write-Host "   - URL: https://dashboard.render.com/web/srv-ABC123DEF456"
Write-Host "   - ID: srv-ABC123DEF456 (parte após /srv-)"
Write-Host ""

Write-Host "3. RENDER_SERVICE_NAME" -ForegroundColor Cyan
Write-Host "   - Nome do seu serviço no Render"
Write-Host "   - Exemplo: roteiro-dispersacao-chatbot"
Write-Host ""

Write-Host "4. RENDER_FRONTEND_SERVICE_NAME (Opcional)" -ForegroundColor Cyan
Write-Host "   - Nome do serviço frontend (se separado)"
Write-Host "   - Exemplo: roteiro-dispersacao-frontend"
Write-Host ""

Write-Host "🔧 Como configurar no GitHub:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. Vá para: https://github.com/AnalineS/roteiro-de-dispersacao-v4/settings/secrets/actions"
Write-Host "2. Clique em 'New repository secret'"
Write-Host "3. Adicione cada secret com o nome e valor corretos"
Write-Host ""

# Extrair informações do repositório
$repoInfo = $remoteUrl -split "/"
$username = $repoInfo[-2]
$repoName = $repoInfo[-1] -replace "\.git$", ""

Write-Host "🔗 Links úteis:" -ForegroundColor Yellow
Write-Host ""

Write-Host "GitHub Secrets:"
Write-Host "https://github.com/$username/$repoName/settings/secrets/actions" -ForegroundColor Blue

Write-Host ""
Write-Host "GitHub Actions:"
Write-Host "https://github.com/$username/$repoName/actions" -ForegroundColor Blue

Write-Host ""
Write-Host "Render Dashboard:"
Write-Host "https://dashboard.render.com" -ForegroundColor Blue

Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. Configure os secrets no GitHub"
Write-Host "2. Faça push das alterações para main/master"
Write-Host "3. Verifique o deploy automático na aba Actions"
Write-Host "4. Monitore os logs do Render"
Write-Host ""

Write-Host "🧪 Teste o deploy:" -ForegroundColor Yellow
Write-Host ""

Write-Host "Após configurar os secrets, você pode:"
Write-Host "1. Fazer um commit e push para testar o deploy automático"
Write-Host "2. Ou ir para Actions → Deploy Automático - Render → Run workflow"
Write-Host ""

Write-Host "✅ Configuração concluída!" -ForegroundColor Green
Write-Host ""

# Verificar se o workflow existe
if (Test-Path ".github/workflows/deploy-automatic.yml") {
    Write-Host "✅ Workflow de deploy automático encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️ Workflow de deploy automático não encontrado" -ForegroundColor Yellow
    Write-Host "   Verifique se o arquivo .github/workflows/deploy-automatic.yml existe" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📞 Para suporte, consulte o arquivo GUIA_CONFIGURAR_SECRETS_RENDER.md" -ForegroundColor Cyan 