@echo off
echo ========================================
echo  DEBUG COMPLETO - CHATBOT TESE HANSENIASE
echo ========================================
echo.

set ISSUES=0
set WARNINGS=0

echo 1. Verificando estrutura de arquivos...
echo ----------------------------------------

REM Verificar arquivos obrigatórios
if exist "index.html" (
    echo ✅ index.html encontrado
) else (
    echo ❌ index.html AUSENTE
    set /a ISSUES+=1
)

if exist "script.js" (
    echo ✅ script.js encontrado
) else (
    echo ❌ script.js AUSENTE
    set /a ISSUES+=1
)

if exist "app_optimized.py" (
    echo ✅ app_optimized.py encontrado
) else (
    echo ❌ app_optimized.py AUSENTE
    set /a ISSUES+=1
)

if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
) else (
    echo ❌ requirements.txt AUSENTE
    set /a ISSUES+=1
)

if exist "optimized_config.json" (
    echo ✅ optimized_config.json encontrado
) else (
    echo ❌ optimized_config.json AUSENTE
    set /a ISSUES+=1
)

REM Verificar arquivos opcionais
if exist "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" (
    echo ✅ PDF encontrado
    for %%A in ("Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf") do (
        set SIZE=%%~zA
        set /a SIZE_MB=!SIZE!/1024/1024
        echo    Tamanho: !SIZE_MB! MB
    )
) else (
    echo ⚠️  PDF AUSENTE (opcional)
    set /a WARNINGS+=1
)

if exist "tese.html" (
    echo ✅ tese.html encontrado
) else (
    echo ⚠️  tese.html AUSENTE (opcional)
    set /a WARNINGS+=1
)

echo.
echo 2. Verificando Python...
echo ----------------------------------------

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado
    python --version
) else (
    echo ❌ Python NAO ENCONTRADO
    echo    Instale Python de: https://www.python.org/downloads/
    set /a ISSUES+=1
)

echo.
echo 3. Verificando dependencias...
echo ----------------------------------------

pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip encontrado
) else (
    echo ❌ pip NAO ENCONTRADO
    set /a ISSUES+=1
)

echo.
echo 4. Verificando conectividade...
echo ----------------------------------------

ping -n 1 google.com >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Conectividade OK
) else (
    echo ❌ Sem conectividade
    set /a ISSUES+=1
)

echo.
echo 5. Verificando configuracoes...
echo ----------------------------------------

if exist "optimized_config.json" (
    echo ✅ Configuração encontrada
    findstr "chunk_size" optimized_config.json >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Configuração válida
    ) else (
        echo ❌ Configuração inválida
        set /a ISSUES+=1
    )
) else (
    echo ❌ Configuração ausente
    set /a ISSUES+=1
)

echo.
echo 6. Verificando scripts de inicialização...
echo ----------------------------------------

if exist "setup.bat" (
    echo ✅ setup.bat encontrado
) else (
    echo ❌ setup.bat AUSENTE
    set /a ISSUES+=1
)

if exist "start.bat" (
    echo ✅ start.bat encontrado
) else (
    echo ❌ start.bat AUSENTE
    set /a ISSUES+=1
)

echo.
echo ========================================
echo  RESULTADO DO DEBUG
echo ========================================

if %ISSUES% equ 0 (
    echo.
    echo 🎉 TODOS OS TESTES PASSARAM!
    echo ✅ O site está pronto para execução
    echo.
    echo 🚀 Para iniciar:
    echo    setup.bat
    echo    start.bat
    echo.
    echo 🌐 Acesse: http://localhost:5000
) else (
    echo.
    echo ❌ %ISSUES% PROBLEMAS ENCONTRADOS:
    echo.
    if %ISSUES% gtr 0 (
        echo 🔧 AÇÕES NECESSÁRIAS:
        echo    - Verifique se todos os arquivos estão presentes
        echo    - Instale Python se necessário
        echo    - Execute: pip install -r requirements.txt
        echo    - Baixe o PDF do link fornecido
    )
)

if %WARNINGS% gtr 0 (
    echo.
    echo ⚠️  %WARNINGS% AVISOS:
    echo    - Alguns arquivos opcionais estão ausentes
    echo    - O site funcionará, mas com funcionalidades limitadas
)

echo.
echo ========================================
pause 