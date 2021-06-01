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
