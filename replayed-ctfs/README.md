# Replayed CTFs

A collected of replayed CTFs and learnings...

## San Diego CTF 2021

### OSINT

- **This flag has been stolen**: use the fact that website archives can be found on the wayback machine

- **Speed Studying**: *Help, I'm studying for a test, and I need you to find an example problem for me... I'm sure you can find it out there somewhere! I'm trying to remember this professor's name but I'm having trouble...who is the only professor at UC San Diego that is both an Assistant Professor for the Computer Science department, and an Associate Professor for the Mathematics department?*

On the [CS faculty page](https://www.sandiego.edu/engineering/programs/computer-science/faculty.php?name_search=&name_search_option=Any&relevancy=contains&sort=&list_view_type=box-view&filter_type=office-department-group&show_image=Yes&details_button=show-details-button&department_filter_type=0&row_limit=24&division_id=NaN&office_department_id=NaN&sub_department_id=160&sub_unit_id=NaN&group_id=5%2C6%2C7%2C8%2C10&scroll=true&filter_action=clicks), there be only one assistant professor: **Jennifer Olsen**. But this was a false positive. The actual result was on UCSD catalog for [computer science](https://catalog.ucsd.edu/faculty/CSE.html) and [Math](https://catalog.ucsd.edu/faculty/MATH.html). `Daniel Kane` is the flag.

### Rev

- **A Bowl of Pythons**: A bowl of spaghetti is nice. What about a bowl of pythons?

Most of the reversing is straightforward in this problem, keep doing the reverse of what it asks you to do. The final part involves a simple XOR cipher; XOR implies given `a = b ^ c` is equivalent to `a ^ c = b`, so reversing is straightforward.

Problems:
	
	- b`xyz` and `xyz`.encode() is equivalent unless it is not. In this case, they are not.

```py
b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4'  =   b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4'

't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4'.encode()  = b't2q}*\x7f&n[5V\xc2\xb42a\x7f3\xc2\xac\xc2\x87\xc3\xa6\xc2\xb4'
```

So these aren't equivalent.

**Flag**: sdctf{v3ry-t4sty-sph4g3tt1}

### Crypto

- **Lost in transmission**: I had my friend send me the flag, but it seems a bit…off.

The given file is a `Non-ISO extended-ASCII text, with no line terminators`. This is most likely a *text* file from the lack of control characters (byte values 0-31) other than line breaks. This is *extended-ASCII* because there are characters outside the ASCII range (byte values >=128). This is *non-ISO* because there are characters in the 128-159 range (ISO 8859 reserves this range for control characters). I tried things like `recode` but it's best to open it with python with open(..., `rb`).

```py
'\xe6\xc8\xc6\xe8\xcc\xf6\xae`\xdc\x88f\xe4\xcc\xaa\x98\xbe\xda\xb2\xbe\x8e``\xc8\xbe\xe6b\xa4\xfa'
```

So anyways, converting this to decimal gives a sequence wherein each integer is twice the value of decimal conversion of the flag `sdctf{W0nD3rfUL_mY_G00d_s1R}`


- **A Prime Hash Candidate**: After the rather embarrassing first attempt at securing our login, our student intern has drastically improved our security by adding more parameters. Good luck getting in now!

```py
PASSWD = 91918419847262345220747548257014204909656105967816548490107654667943676632784144361466466654437911844

def hash(data):
    out = 0
    data = [ord(x) ^ ord(y) for x,y in zip(data,secret1*len(data))]
    data.extend([ord(c) for c in secret2])
    for c in data:
        out *= secret3
        out += c
    return out

if hash(data) == PASSWD:
    print(SUCCESS)
    break
```
Note how `out` is built incrementally. `zip` simply returns tuples (first character of data mapped with first character of secret), multiplication with `len(data)` simply increases the length. Extend simply adds things to the end of the list. We know the first few characters: `sdctf{`. We can figure out things.

[Solution but I didn't understand it](https://qiita.com/mikecat_mixc/items/5a0c45751b15c8a8513b). But important points:

- Guessed the multiplier through ratio of the hashed values (since the hash values are effectively summed up)

- Then using remainders, the rest of the things was guessed.

- It's an adaptive attack. The attacker is able to get hashes of chosen plaintexts.
