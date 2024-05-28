import smtplib
from email.mime.text import MIMEText

# Configurações do servidor de e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "trabalhoredes71@gmail.com"
PASSWORD = "sbgi wrzw adba ceme"

# Configurações do destinatário
TO_EMAIL = "wtironi@gmail.com"

# Criar mensagem de e-mail
msg = MIMEText("Este é um e-mail de teste!")
msg['Subject'] = "E-mail de teste"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# Conectar ao servidor de e-mail
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(FROM_EMAIL, PASSWORD)

# Enviar e-mail
server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
server.quit()

print("E-mail enviado com sucesso!")