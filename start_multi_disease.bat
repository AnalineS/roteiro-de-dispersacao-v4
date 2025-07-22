@echo off
echo ========================================
echo    INICIANDO CHATBOT MULTI-DOENCAS
echo ========================================
echo.

echo Verificando arquivos necessarios...
if not exist "app_multi_disease.py" (
    echo ERRO: app_multi_disease.py nao encontrado!
    pause
    exit /b 1
)

if not exist "PDFs" (
    echo Criando pasta PDFs...
    mkdir PDFs
)

echo.
echo Verificando PDFs disponiveis...
set pdf_count=0
for %%f in (PDFs\*.pdf) do (
    set /a pdf_count+=1
    echo - %%f
)

if %pdf_count%==0 (
    echo.
    echo AVISO: Nenhum PDF encontrado na pasta 'PDFs'
    echo O chatbot funcionara apenas com respostas padrao
    echo.
    echo Para adicionar PDFs:
    echo 1. Baixe os PDFs das doencas
    echo 2. Coloque-os na pasta 'PDFs'
    echo 3. Renomeie para: hanseniase.pdf, diabetes.pdf, hipertensao.pdf
    echo.
)

echo.
echo Iniciando servidor...
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar
echo.

python app_multi_disease.py

pause 