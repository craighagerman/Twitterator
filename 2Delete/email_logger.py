
import json
import logging
from logging.handlers import *
import os
import smtplib

class EmailLogger:
    def __init__(self, credentials_file):
        keys = json.load(open(credentials_file))
        self.server = keys['server']
        self.port = keys['port']
        self.from_address = keys['from_address']
        self.username = keys['username']
        self.password = keys['password']
        self.to_address_list = keys['to_address_list']
        self.log_dir = keys['log_dir']
        self.subject = keys['subject']


    def create_logger(self, identifier):
        """
        Creates a rotating log
        level can be one of logging.DEBUG logging.INFO logging.WARNING logging.ERROR  logging.CRITICAL
        """
        logger = logging.getLogger()
        logfile = "{}_log.txt".format(identifier)
        
        # Send an email about everything above level WARN (alternately could be ERROR)
        handler = TLSSMTPHandler((self.server, self.port), self.from_address, self.to_address_list, self.subject, (self.username, self.password))
        handler.setLevel(logging.WARN)
        formatter = logging.Formatter("[%(levelname)s]  %(asctime)s [{}]: %(message)s".format(identifier), datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Log everything above INFO level to the spcified logfile
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(os.path.join(self.log_dir, logfile), backupCount=5)
        formatter = logging.Formatter("[%(levelname)s]  %(asctime)s [{}]: %(message)s".format(identifier), datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


class TLSSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addressees.
        """
        try:
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
                            self.fromaddr,
                            ",".join(self.toaddrs),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
 


 