import ftplib
import os
import socket
HOST='210.45.66.132:21007'
USER='jiangsu'
PASS='Jiangsu@2019'
DIRN=''
FILE=''
try:
    f=ftplib.FTP(HOST,USER,PASS)
except (socket.error,socket.gaierror),e:
    print 'ERROR:cannot reach "%s"' % HOST)
print '** Connected to host "%s"' % HOST)
try :
    f.login()
except ftplib.error_perm:
    print('ERROR: cannot login')
    f.quit()
print('*** Logged in ')
try:
    f.cwd(DIRN)
except ftplib.error_perm:
    print('ERROR: cannot CD to "%s"' % DIRN)
    f.quit()
print('ERROR: cannot CD to "%s"' % DIRN)
try:
    f.retrbinary('RETR s%' % FILE,open(FILE,'wb').write)
except ftplib.error_perm:
    print('ERROR')
    os.unlink(FILE)
else:
    print('*** Downloaded "%s' to CED' % FILE)
f.quit()
