import pexpect, sys

user = sys.argv[1]
password = sys.argv[2]
cmmd = sys.argv[3]

child = pexpect.spawn(cmmd)
child.logfile = sys.stdout
child.expect_exact('[sudo] password for '+user+': ')
child.sendline(password)

child.expect_exact('Do you want to continue? [Y/n] ')
child.sendline('Y')

child.expect(pexpect.EOF, timeout=None)