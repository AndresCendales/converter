import os
import smtplib

sender = "Coverter <notifier@converter.com>"
receivers = ['Andres Cendales <andres01660@gmail.com>'
             ]


class Notifier:
    def send_notification_to_download(self, original_file_path, new_format, new_file_path):
        self.get_email(original_file_path, new_format, new_file_path)
        self.send_notification(self.email, os.getenv("MAILGUN_PASSWORD"))
        return "email sent.", 200

    def get_email(self, original_file_path, new_format, new_file_path):
        subject = "Converted document!"

        own_message = """Hi! <br/> <br/> 
        The document that you uploaded in the route <b>%s</b>, to be converted to one of a kind <b>%s</b> 
        it's ready, you can find it with on the route <b>%s</b>
        <br/> <br/>
        Best regards from Converter.
        """ % (original_file_path, new_format, new_file_path)

        self.email = """From: %s 
        To: %s 
        MIME-Version: 1.0 
        Content-type: text/html 
        Subject: %s 
        %s
        """ % (sender, receivers, subject, own_message)

    def send_notification(self, email, smtp_password):
        try:
            s = smtplib.SMTP(host='smtp.mailgun.org', port=587)
            s.starttls()
            s.login("postmaster@sandbox5a390ccc8a52448fa5a7f8c6d603e025.mailgun.org", smtp_password)
            s.sendmail(sender, receivers, email)
            print("email sent")
        except Exception as e:
            print(e)
            print("Error: the message could not be sent. Check that sendmail is installed on your system")
