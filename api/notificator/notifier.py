import smtplib

sender = "Coverter <notifier@converter.com>" 
receivers = ['Anderson Santamaria <andersonsantamaria3@gmail.com>'
    ]

def get_email(username, original_file_path, new_format, new_file_path):  
    subject = "Converted document!"
    
    own_message = """Hi! %s<br/> <br/> 
The document that you uploaded in the route <b>%s</b>, to be converted to one of a kind <b>%s</b> 
it's ready, you can find it with on the route <b>%s</b>
<br/> <br/>
Best regards from Converter.
""" % (username, original_file_path, new_format, new_file_path)

    email = """From: %s 
To: %s 
MIME-Version: 1.0 
Content-type: text/html 
Subject: %s 
%s
""" % (sender, receivers, subject, own_message)
    return email

def send_notification(email, smtp_password):
    try: 
        s = smtplib.SMTP(host='smtp.mailgun.org', port=587)
        s.starttls()
        s.login("postmaster@sandbox5a390ccc8a52448fa5a7f8c6d603e025.mailgun.org", smtp_password)
        s.sendmail(sender, receivers, email) 
        print("email sent") 
    except Exception as e: 
        print(e)
        print("Error: the message could not be sent. Check that sendmail is installed on your system")

class Notifier():
    def send_notification_to_download(self, username, original_file_path, new_format, new_file_path):
        email = get_email(username, original_file_path, new_format, new_file_path)
        send_notification(email, "pass")
        return "email sent.", 200