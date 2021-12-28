# generate a SSL/TLS certificate
#

import os
import sys
import subprocess


# generate a SSL/TLS certificate with 365 days rsa fo 2048 and not encrypted without a password and without a domain
def generate_certificate():
    command = "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem"
    subprocess.call(command, shell=True)
    print("Certificate generated")
    # print the certificate
    command = "openssl x509 -in certServ.pem -text -noout"
    subprocess.call(command, shell=True)
    print("Certificate printed")





if __name__ == '__main__':
    generate_certificate()
    print("End of program")
    sys.exit(0)
