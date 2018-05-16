# -*- coding: utf-8 -*

import tweepy, config, smtplib
import time

# Config values
email_from = config.email_from
email_cc = config.email_cc
email_to = config.email_to
email_smtp_server = config.email_smtp_server
email_smtp_server_port = int(config.email_smtp_server_port)



# Mandar emails
def sendEmail():
	
	toaddr = [email_to]
	cc = [email_cc]
	fromaddr = email_from
	
	message_subject = "Twitter alert"
	#############################
	msg_aux = ("Alerta uso twitter fuera de horario \n\nHora:\t"+"a")
	message_text = msg_aux.encode("utf-8")
	############################

	message = "From: %s\r\n" % fromaddr + "To: %s," % toaddr[0][0]+"%s\r\n"% toaddr[0][1]+ "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % message_subject + "\r\n"  + message_text
	toaddrs = [toaddr] + cc
	server = smtplib.SMTP(email_smtp_server, int(email_smtp_server_port))
	
	server.sendmail(email_from, toaddr[0], message)
	#server.sendmail(email_from, toaddr[0][1], message)
	server.sendmail(email_from, email_cc, message)
	


def main():
	sendEmail()

if __name__ == "__main__":
    main()
