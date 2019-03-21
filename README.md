# CertHandler Project
CertHandler automates the process of installing, creating, and displaying certificates for you.

## Getting Started

These instructions will get you a copy of the project up and running on your machine for development and testing purposes. 

### Prerequisites
	Operating System - Fedora 29 - https://getfedora.org/en/workstation/download/
	Python - 3.0+ /url "https://www.python.org/downloads/"
	Directory Server - https://www.dogtagpki.org/wiki/Installing_DS#References 
	Certificate Authority - https://github.com/dogtagpki/pki/blob/master/docs/installation/Installing_CA.md#verifying-system-certificates
	
	Tools:

	1. DNF
	
	Python Libraries

	1. os
	2. socket	
	3. datetime
	4. logging
	5. subprocess

### How to run

	1. Create a file ca.cfg (present in the repository)
	2. Run the file automate.py from CLI using the command 
	   
	  $ sudo python automate.py

### Design Details:

	1. automate.py - Main File to run
	2. ca.cfg - Deployment Configuration File
	3. Log/ - Included to show log from a trial run
	4. Output/ - Included to show output files (including certificate) created after running the script

### Process Abstract:

	The automate.py file automates the process of installing DS, CA, creates and displays a certificate.
	
	1. Installs DS
	2. Installs CA
	3. Verifies the System and Admin Certificates
	4. Prepares the User
	5. Requests for Certificate
	6. Approval of the Certificate Request by the CA Agent
	7. Assigning the certificate to the user by an admin
	8. Download the certificate 
	9. Import it into the security database 
	10. Displaying the Certificate
	

## License
MIT License

Copyright (c) [2019] [Sneha Veeranki]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



