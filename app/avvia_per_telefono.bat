@echo off
title Avvocato del Diavolo - Modalita Telefono e Computer
echo ============================================================
echo   AVVOCATO DEL DIAVOLO - Modalita Rete per Telefono
echo ============================================================
echo.
echo Quando vedi "Network URL: http://...", copia quell'indirizzo
echo nel browser del tuo smartphone (connesso allo stesso Wi-Fi).
echo.
streamlit run app.py --server.address 0.0.0.0
pause
