# 🚀 DEPLOY AUTOMATICO - NETLIFY 
 
## ✅ Arquivo ZIP Criado: deploy_automatico.zip 
 
### Passo a Passo: 
1. Acesse: https://app.netlify.com/ 
2. Clique em "Add new site" 
3. Selecione "Deploy manually" 
4. Arraste o arquivo deploy_automatico.zip 
5. Configure: 
   - Build command: bash netlify_build_fix.sh 
   - Publish directory: . 
   - Functions directory: functions 
   - Python version: 3.9 
6. Clique em "Deploy site" 
