from app_serial import app_serial

#Inicializar o app de leitura serial
app = app_serial()
app.check_equipamento()
app.open_serial()