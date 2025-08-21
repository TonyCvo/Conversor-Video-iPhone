@echo off
echo ========================================
echo   Conversor de Video - Instalacao
echo ========================================
echo.

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo   Instalacao concluida!
echo ========================================
echo.
echo Para executar o conversor:
echo python "Converter MPG em MOV.py"
echo.
echo Certifique-se de que o FFmpeg esta instalado
echo e configurado no PATH do sistema.
echo.
pause
