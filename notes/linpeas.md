# LINPEAS

Amazing tool at [Github](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS)

Amazing book at [HackTricks](https://book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist)

Some information I obtained by running and researching linpeas result on HackTheBox machines:

- [`AppArmor`](https://www.kernel.org/doc/html/v4.15/admin-guide/LSM/apparmor.html): Security extension for the linux kernel. It allows the system administrator to restrict programs' capabilities with per-program profiles. Profiles can allow capabilities like network access, raw socket access, and the permission to read, write, or execute files on matching paths. Search for it in `/etc/apparmor.d`.

- [`ASLR`](https://blog.morphisec.com/aslr-what-it-is-and-what-it-isnt/): involves randomly positioning the base address of an executable and the position of libraries, heap, and stack, in a process's address space. ASLR is `address space layout randomization`. Rather than removing things, ASLR makes it difficult to exploit existing things because you no longer know the default positioning of things. Recent version is `Moving Target Defense`