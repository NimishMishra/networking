# New command line options learnt. Use --help for details

tr: translate, delete 

uniq: unique lines in a file

strings: display printable strings in files

base64: encoding, decoding

tar, gz, bzip2: compression 

xxd: reverse hexdump (see challenge 12)

# Level 0: 


Host: bandit.labs.overthewire.org
Port: 2220

Initial connection: ssh bandit0@bandit.labs.overthewire.org -p 2220

Password for level 0: bandit0


cat readme

Password for level 1: boJ9jbbUNNfktd78OOpsqOltutMc3MY1

# Level 1: 

Connection: ssh bandit1@bandit.labs.overthewire.org -p 2220

Since the filename is a special character, it is opened using cat ./- [Source](https://stackoverflow.com/questions/42187323/how-to-open-a-f-dashed-filename-using-terminal)

Password for level 2: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9

# Level 2 

Connection: ssh bandit2@bandit.labs.overthewire.org -p 2220

Filename has spaces. A simple cat 'file name' does the trick.

Password for level 3: UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK

# Level 3

ssh bandit3@bandit.labs.overthewire.org -p 2220

The file is hidden. A simple ls -la reveals the file .hidden. Then a simple cat '.hidden'

Password for level 4: pIwrPrtPN36QITSp3EQaw936yaFoFgAB

# Level 4

ssh bandit4@bandit.labs.overthewire.org -p 2220

## A simple solution 

cat ./-file07

## Python solution

file_list = [x for x in os.listdir(os.getcwd())]

for i in file_list:
    file_object = open(i, 'r')
    print(file_object.read())

All non human-readable files will give errors in decoding utf-8. Only the one with worth decoding gives the password

Password: koReBOKuIDDepwhWk7jZC0RTdopnAYKh

# Level 5

ssh bandit5@bandit.labs.overthewire.org -p 2220

Find a file human readable, size 1033 bytes, and non-executable.

find . -type f -size 1033c -readable ! -executable

find . -type f -size 1033c ! -executable

Password: DXjZPULLxYr17uwoI01bNLQbtFemEgo7

# Level 6

ssh bandit6@bandit.labs.overthewire.org -p 2220

The main trick was to search in the entire server. Accomplished by find / -user bandit7 -group bandit6 -size 33c instead of find . -user bandit7 -group bandit6 -size 33c

Password: HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs

# Level 7

ssh bandit7@bandit.labs.overthewire.org -p 2220

In a huge file, password was next to the word 'millionth'

## Simple solution

cat data.txt | grep millionth

## Python solution

data = open('data.txt', 'r').read()
print(data[data.index('millionth'):data.index('millionth')+100])

Password: cvX2JJa4CFALtqS87jk27qwqGhBM9plV

# Level 8

ssh bandit8@bandit.labs.overthewire.org -p 2220

In a huge file, find the only line of text that occurs only once. A simple grep without duplicates should do. Or better, unique command on sorted file.

sort data.txt | uniq -u

UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

# Level 9

ssh bandit9@bandit.labs.overthewire.org -p 2220

A semi human readable file containing lots of things. Password was ============== followed by the password. I used strings -d -n 40 data.txt to extract that line (-d means to look only at the data section. -n means to have 40 bytes).

Another approach: strings data.txt | grep "="

truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

# Level 10

ssh bandit10@bandit.labs.overthewire.org -p 2220

The file was base 64 encoding. A simple cat data.txt | base64 -d decoded the entire thing.

Password: IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR

# Level 11

ssh bandit11@bandit.labs.overthewire.org -p 2220

Decoding a rot13 cipher in linux. Perfect task for tr. cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' Note how the rotataions happen

Password: 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

# Level 12

ssh bandit12@bandit.labs.overthewire.org -p 2220

A hexdump file was compressed several times. The basic idea is to use xxd to reverse hexdump and store with original format. Let's say gzip compression. Convert filename mv data data.gz and run gzip -d data.gz. Now check file data, you get bzip file. Convert again mv data data.bz and run bzip2 -d data.bz. Do this again and again until you reach ASCII text.

tar -xf data6, mx data8.bin data8.gz, gzip -d data8.gz, 

Password: 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

# Level 13

ssh bandit13@bandit.labs.overthewire.org -p 2220
