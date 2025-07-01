#!/bin/bash

# ThunderSpoof Lab SMTP Installer
set -e

echo "[+] Updating system..."
sudo apt update && sudo apt install postfix mailutils -y

echo "[+] Configuring Postfix..."

echo "postfix postfix/mailname string labspoof.local" | sudo debconf-set-selections
echo "postfix postfix/main_mailer_type string 'Internet Site'" | sudo debconf-set-selections

sudo tee /etc/postfix/main.cf > /dev/null <<EOF
smtpd_banner = \$myhostname ESMTP ThunderSpoof Lab
biff = no
append_dot_mydomain = no
readme_directory = no

myhostname = labspoof.local
myorigin = /etc/mailname
mydestination = \$myhostname, localhost.\$mydomain, localhost
relay_domains = \$mydomain

# Restrict relay to local subnet - customize to your network
mynetworks = 127.0.0.0/8, 192.168.0.0/16

mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = ipv4

smtpd_recipient_restrictions = permit_mynetworks, reject_unauth_destination
EOF

echo "[+] Restarting Postfix..."
sudo systemctl restart postfix

echo "[✓] Postfix Lab SMTP Server installed and running."
echo "Make sure to allow port 25 through your firewall and restrict access."
