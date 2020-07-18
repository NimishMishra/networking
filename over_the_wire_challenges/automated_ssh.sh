#!/bin/bash
### Auto SSH Wargame Script ###
#NIKHIL JEEWA

sshAccess(){ 
	sshpass -f ./tmp/pass.txt ssh -o StrictHostKeyChecking=no bandit$1@bandit.labs.overthewire.org -p2220 $2
} 

sshCopy(){
	sshpass -f ./tmp/pass.txt scp -P 2220 bandit$1@bandit.labs.overthewire.org:$2 $3
}

autoSSH(){
	#level 0
	echo "bandit 0"
	# mkdir ~/otw/tmp/pass
	echo "bandit0"> ./tmp/pass.txt
	sshAccess 0 'ls -a'
	sshCopy 0 /home/bandit0/readme ./tmp
	mv ./tmp/readme ./tmp/pass.txt
	echo "bandit 1 password is: $(<./tmp/pass.txt)"
	
	#level 1
	sshAccess 1 'ls'	
	sshCopy 1 /home/bandit1/./- ./tmp
	mv ./tmp/./- ./tmp/pass.txt
	echo "bandit 2 password is: $(<./tmp/pass.txt) "

	#level 2
	sshAccess 2 'ls; mkdir /tmp/smtclabc; cp "spaces in this filename" /tmp/smtclabc/pass'
	sshCopy 2 /tmp/smtclabc/pass ./tmp
	sshAccess 2 'rm -r /tmp/smtclabc'
#	sshpass -f ~/otw/tmp/pass  scp -P 2220 "bandit2@bandit.labs.overthewire.org:/home/bandit2/spaces\ in\ this\ filename" ~/otw/tmp
	
	
	echo "bandit 3 password is: $(<./tmp/pass) "

#	rm -r ~/otw/tmp
}
autoSSH;