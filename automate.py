import os
import socket
import subprocess
import logging
import datetime

def exitOrNot(returnCode, msg,exitFlag):
	if returnCode == 0:
		logging.info(msg+' - Successful')
	elif returnCode != 0 and exitFlag:
		logging.error(msg+' - Failed')
		exit()
	elif returnCode != 0 and not exitFlag:
		logging.warning('Issues with '+msg)



#logging the process
filename = datetime.datetime.now().strftime("%d-%B-%Y_%I:%M%p")+'.log'
logging.basicConfig(level=logging.DEBUG,filename=filename, filemode='w', format='%(levelname)s-%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('Logging of CertHandler Begins')

#Install DS
dnf_check = os.system('dnf install -y 389-ds-base')
exitOrNot(dnf_check,"389-ds-base installation",True)
	

#Generate a configuration template
dscreate1_chk = os.system('dscreate create-template ds.tmp')
exitOrNot(dscreate1_chk,"dscreate setup",True)

#Customize the configuration template
sed_chk = os.system( "sed \
    -e \'s/;root_password = .*/root_password = Secret.123/g' \
    -e \'s/;suffix = .*/suffix = dc=example,dc=com/g' \
    ds.tmp > ds.inf")
exitOrNot(dnf_check,"Customizing Configuration Template",True)

#To create an instance
dscreate2_chk = os.system("dscreate from-file ds.inf")
if dscreate2_chk == 256:
	logging.info("Another instance with the same name may be present")

exitOrNot(dscreate2_chk,"Creating an Instance",False)


#To add base entries
base_chk = os.system("""ldapadd -h $HOSTNAME -x -D \"cn=Directory Manager"\ -w Secret.123 << EOF
dn: dc=example,dc=com
objectClass: domain
dc: example

dn: dc=pki,dc=example,dc=com
objectClass: domain
dc: pki
EOF""")

if base_chk==256:
	logging.info("Base Entries must be already present")
exitOrNot(base_chk,"Adding Base Entries",False)

#Verifying that the FQDN is correctly reported
print(socket.getfqdn())
logging.info('FQDN is '+socket.getfqdn())

#CA Subsystem Installation
pkispawn_chk = os.system('pkispawn -f ca.cfg -s CA')
exitOrNot(pkispawn_chk,"CA Subsystem Installation",False)

#Verifying System Certificates
system_chk = os.system('certutil -L -d /etc/pki/pki-tomcat/alias') 
exitOrNot(system_chk,"Verifying system certificate",False)

#Verifying Admit Certificate Steps
#Prepare a client NSS database (e.g. ~/dogtag/nssdb)
admit_chk = os.system('pki -c Secret.123 client-init')
exitOrNot(admit_chk,"Verifying admit certificate",False)

#Import the CA signing certificate
ca_chk = os.system('pki -c Secret.123 client-cert-import "CA Signing Certificate" --ca-cert /root/.dogtag/pki-tomcat/ca_admin.cert')
exitOrNot(ca_chk,"Import CA signing certificate",False)

#Import admin key and certificate
admin_chk = os.system('pki -c Secret.123 client-cert-import \
 --pkcs12 /root/.dogtag/pki-tomcat/ca_admin_cert.p12 \
 --pkcs12-password-file /root/.dogtag/pki-tomcat/ca/pkcs12_password.conf')
exitOrNot(admin_chk,"Import admin key and certificate",False)

#User Certificate Setup Steps
#Preparing the User
user_chk = os.system('pki -d /root/.dogtag/pki-tomcat/ca/alias -c Secret.123 -n caadmin \
    ca-user-add testuser --fullName \"Test User"\ ')
exitOrNot(user_chk,"User certificate setup",False)

#Add the user to the appropriate groups
group_chk = os.system('sudo pki -d /root/.dogtag/pki-tomcat/ca/alias -c Secret.123 -n caadmin ca-group-member-add "Certificate Manager Agents" testuser')
exitOrNot(group_chk,"Adding user to group",False)

#As the user, prepare a security database
database_chk = os.system('pki -c Secret.123 client-init')
exitOrNot(database_chk,"Preparing a security database",False)

#As the user, generate and submit a certificate request
request = subprocess.check_output('pki -c Secret.123 client-cert-request uid=testuser', shell=True)

if "Request ID:" in request:
	request_id = request.split('\n')[3].split()[2]
	logging.info("Created request id is "+request_id)
else:
	logging.info("Issue with certificate request")

#As a CA agent, approve the request
try:
	approve_rslt = subprocess.check_output('pki -d /root/.dogtag/pki-tomcat/ca/alias -c Secret.123 -n caadmin ca-cert-request-review '+ request_id+' --action approve', shell=True)
except subprocess.CalledProcessError as grepexc:
	logging.info("error code", grepexc.returncode, grepexc.output)

cert_id = approve_rslt.split('\n')[7].split()[2]
logging.info("Created certificate id is "+cert_id)

#As an admin of the subsystem assign the certificate to the user
assign_certi = os.system('pki -d /root/.dogtag/pki-tomcat/ca/alias -c Secret.123 -n caadmin \
    ca-user-cert-add testuser --serial '+cert_id)
exitOrNot(assign_certi,"Assigning the certificate to the user as the admin",False)

#To download the certificate
download_certi = os.system('pki ca-cert-show '+cert_id+' --output testuser.crt')
exitOrNot(download_certi,"Downloading the certificate",False)

#To assign the certificate to the user:
assign_certi2 = os.system('pki -d /root/.dogtag/pki-tomcat/ca/alias -c Secret.123 -n caadmin \
    ca-user-cert-add testuser --input testuser.crt')
exitOrNot(assign_certi2,"Assigning the certificate to the user",False)

#Retrieving the Certificate
#As the user, download the certificate and import it into the security database
get_certi = os.system('pki -c Secret.123 client-cert-import testuser --serial '+cert_id)
exitOrNot(get_certi,"Retrieving the Certificate",False)

#Displaying the Certificate
show_certi = os.system('pki ca-cert-show '+cert_id)
exitOrNot(show_certi,"Displaying the Certificate",False)



