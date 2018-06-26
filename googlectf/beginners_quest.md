# Beginner's Quest

##### Done in collaboration with [labeebabegum](https://github.com/labeeba)

### Letter

We got a `pdf` from the quest zip file. We copied the part that we saw in the hidden field next to password. We copied the hidden field and pasted it into notepad. This gave us the flag.

### OCR IS COOL

Once we saw `Caesar`, we thought it was a `caesar cipher`. We retrieved a screen-shot from the quest site. On the screen-shot, we looked for a part that would read like `XXX{...}`. When we found it the following gave the flag:

```bash
$ echo VMY{vtxltkvbiaxkbltlnulmbmnmbhgvbiaxk} | tr [V-ZA-Uv-za-u] [C-ZABc-zab]
# seeing V, it was easy to construct the tr command from there
# start with V, go till Z and start over at A
```



### Security by Obscurity

As soon as we saw "John" in the description, we thought this might be a brute force problem. The better hint was `security by obscurity` on the title. Once the file was downloaded and unzipped, the file had a `.p` extension. Running the `file` command on the file reveals that it is a `zip` file. We ran the following command a few times until we got an error:

```sh
$ unzip `ls | head -1`
```

After it reaches second `.a` file an error is thrown. Running the `file` command again reveals the the file is a `xz compressed data` file. The following sequence of command was run to extract files further:

```bash
$ xz -d -S .a `ls | head -1`
$ xz -d -S .b `ls | head -1`
$ xz -d -S .c `ls | head -1`
$ xz -d -S .d `ls | head -1`
$ xz -d -S .e `ls | head -1`
$ xz -d -S .f `ls | head -1`
$ xz -d -S .g `ls | head -1`
$ xz -d -S .h `ls | head -1`
$ xz -d -S .i `ls | head -1`
$ xz -d -S .j `ls | head -1`
$ xz -d -S .k `ls | head -1`
$ xz -d -S .l `ls | head -1`
$ xz -d -S .m `ls | head -1`
$ xz -d -S .n `ls | head -1`
$ xz -d -S .o `ls | head -1`
$ xz -d -S .p `ls | head -1`
```

The `-S` option is necessary to recognize that suffix as valid `xz` file. Next we can use the `flag` command again to see that the extracted file is now `bzip2` file. To decompress, we used the following command:

```bash
$ cp pass<tab> aaaa
$ bzip2 -d `ls | head -1` #this command is run until we hit an error
# once the error is hit, we get an aaaa.out.out....out file
# so we lose track of how much closer we are but that's okay
```

Next we run the `file` command again. It reveals the file is `gzip` compressed. We run the following command to extract file. After this, we ran the following command a few times:

```bash
$ mv aaaa.out<tab> aaaa
$ # repeat the following command until an error is hit
$ mv aaaa aaaa.gz && gzip -d aaaa.gz
```

Here if we run the `file` command we get a `zip` file that would expand to `password.txt`. One can assume that the flag is in there. However, the zip file is password protected. We used `John The Ripper` to crack the password. The following commands were used:

```bash
$ mv aaaa.gz password.zip 
$ zip2john password.zip > password.hash
$ john password.hash
```

 ### MOAR

We are given the man page. All we have to do is `!command` to run the command on man page. The following should reveal the flag:

```bash
$ nc moar.ctfcompetition.com 1337
...
Manual Page ... (quit) !ls
...
Manual Page ... (quit) !ls /home/moar
...
Manual Page ... (quit) !ls /home/moar/disable_dmz.sh
# this should reveal the flag
```

 