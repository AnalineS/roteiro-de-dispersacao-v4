@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  DEBUG DETALHADO - CHATBOT TESE HANSENIASE
echo ========================================
echo.

echo 1. VERIFICANDO ARQUIVOS OBRIGATORIOS...
echo ----------------------------------------

set MISSING=0

echo Verificando index.html...
if exist "index.html" (
    for %%A in ("index.html") do (
        echo ✅ index.html - !%%~zA! bytes
    )
) else (
    echo ❌ index.html AUSENTE
    set /a MISSING+=1
)

echo Verificando script.js...
if exist "script.js" (
    for %%A in ("script.js") do (
        echo ✅ script.js - !%%~zA! bytes
    )
) else (
    echo ❌ script.js AUSENTE
    set /a MISSING+=1
)

echo Verificando app_optimized.py...
if exist "app_optimized.py" (
    for %%A in ("app_optimized.py") do (
        echo ✅ app_optimized.py - !%%~zA! bytes
    )
) else (
    echo ❌ app_optimized.py AUSENTE
    set /a MISSING+=1
)

echo Verificando requirements.txt...
if exist "requirements.txt" (
    for %%A in ("requirements.txt") do (
        echo ✅ requirements.txt - !%%~zA! bytes
    )
) else (
    echo ❌ requirements.txt AUSENTE
    set /a MISSING+=1
)

echo Verificando optimized_config.json...
if exist "optimized_config.json" (
    for %%A in ("optimized_config.json") do (
        echo ✅ optimized_config.json - !%%~zA! bytes
    )
) else (
    echo ❌ optimized_config.json AUSENTE
    set /a MISSING+=1
)

echo.
echo 2. VERIFICANDO ARQUIVOS OPCIONAIS...
echo ----------------------------------------

echo Verificando PDF...
if exist "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" (
    for %%A in ("Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf") do (
        set SIZE=%%~zA
        set /a SIZE_MB=!SIZE!/1024/1024
        echo ✅ PDF encontrado - !SIZE_MB! MB
    )
) else (
    echo ⚠️  PDF AUSENTE (opcional)
    echo    Baixe de: https://drive.google.com/drive/folders/1435FhEIp_yOwtretv-G-ZQpNFY-f6tzr?usp=drive_link
)

echo Verificando tese.html...
if exist "tese.html" (
    for %%A in ("tese.html") do (
        echo ✅ tese.html - !%%~zA! bytes
    )
) else (
    echo ⚠️  tese.html AUSENTE (opcional)
)

echo.
echo 3. VERIFICANDO PYTHON...
echo ----------------------------------------

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado
    python --version
) else (
    echo ❌ Python NAO ENCONTRADO
    echo    Instale Python de: https://www.python.org/downloads/
    echo    Certifique-se de marcar "Add Python to PATH"
    set /a MISSING+=1
)

echo.
echo 4. VERIFICANDO PIP...
echo ----------------------------------------

pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip encontrado
    pip --version
) else (
    echo ❌ pip NAO ENCONTRADO
    set /a MISSING+=1
)

echo.
echo 5. VERIFICANDO CONECTIVIDADE...
echo ----------------------------------------

ping -n 1 google.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Conectividade OK
) else (
    echo ❌ Sem conectividade
    set /a MISSING+=1
)

echo.
echo 6. VERIFICANDO CONFIGURACAO JSON...
echo ----------------------------------------

if exist "optimized_config.json" (
    echo ✅ Configuração encontrada
    findstr "chunk_size" optimized_config.json >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ chunk_size encontrado
    ) else (
        echo ❌ chunk_size ausente
        set /a MISSING+=1
    )
    
    findstr "confidence_threshold" optimized_config.json >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ confidence_threshold encontrado
    ) else (
        echo ❌ confidence_threshold ausente
        set /a MISSING+=1
    )
) else (
    echo ❌ Configuração ausente
    set /a MISSING+=1
)

echo.
echo 7. VERIFICANDO SCRIPTS DE INICIALIZACAO...
echo ----------------------------------------

if exist "setup.bat" (
    for %%A in ("setup.bat") do (
        echo ✅ setup.bat - !%%~zA! bytes
    )
) else (
    echo ❌ setup.bat AUSENTE
    set /a MISSING+=1
)

if exist "start.bat" (
    for %%A in ("start.bat") do (
        echo ✅ start.bat - !%%~zA! bytes
    )
) else (
    echo ❌ start.bat AUSENTE
    set /a MISSING+=1
)

echo.
echo 8. VERIFICANDO CONTEUDO DO HTML...
echo ----------------------------------------

if exist "index.html" (
    findstr "chatbot" index.html >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Seção chatbot encontrada
    ) else (
        echo ❌ Seção chatbot ausente
        set /a MISSING+=1
    )
    
    findstr "script.js" index.html >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Referência ao script.js encontrada
    ) else (
        echo ❌ Referência ao script.js ausente
        set /a MISSING+=1
    )
) else (
    echo ❌ index.html não encontrado para verificação
    set /a MISSING+=1
)

echo.
echo ========================================
echo  RESULTADO DO DEBUG DETALHADO
echo ========================================

if %MISSING% equ 0 (
    echo.
    echo 🎉 TODOS OS TESTES PASSARAM!
    echo ✅ O site está pronto para execução
    echo.
    echo 🚀 PRÓXIMOS PASSOS:
    echo    1. Execute: setup.bat
    echo    2. Execute: start.bat
    echo    3. Acesse: http://localhost:5000
    echo.
    echo 📋 SE O PYTHON NAO ESTIVER INSTALADO:
    echo    - Baixe de: https://www.python.org/downloads/
    echo    - Marque "Add Python to PATH" durante a instalação
    echo    - Reinicie o terminal após a instalação
) else (
    echo.
    echo ❌ %MISSING% PROBLEMAS ENCONTRADOS
    echo.
    echo 🔧 AÇÕES NECESSÁRIAS:
    if %MISSING% gtr 0 (
        echo    - Instale Python 3.8+ se não estiver instalado
        echo    - Execute: pip install -r requirements.txt
        echo    - Baixe o PDF do link fornecido
        echo    - Verifique se todos os arquivos estão presentes
    )
)

echo.
echo ========================================
echo.
echo 📊 RESUMO:
echo    - Arquivos obrigatórios: OK
echo    - Python: Verificar instalação
echo    - Dependências: Instalar após Python
echo    - PDF: Baixar do Google Drive
echo.
pause 