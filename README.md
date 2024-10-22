Bootstrapping LFS 12.2 (SystemD) with RPM
=========================================

This git contains the RPM spec files and text sources/patches not retrievable
easily from a hyperlink for RPM bootstrapping my LFS 12.2 SystemD system.

The is ‘Phase Four’ of [`THE-PLAN.md`](THE-PLAN.md).

Many of the spec files are ported from my previous (incomplete) RPM bootstrap of
my LFS 11.3 SysV Init system but due to a hard drive failure, some of those RPM
spec files were lost and I need to start over.

The RPM spec files committed today (20 October 2024 UTC) all build *except* for
the GCC RPM which is being worked on. With GCC, currently there are installed
files that need to be put into the correct place. Also, I need to add `m2` to
the list of compilers and create a sub-package for it.

(*update: gcc spec file now builds*)

The Perl spec file builds packages but needs to be split up into lots of smaller
packages. For RPM bootstrapping, that does not matter. That is a lot of tedious
work but the value is a small bug fix in a bundled module can then be updated
via RPM without needing to rebuild all of Perl.

The GLibC spec file initially had a bug. Other packages detect they need
`rtld(GNU_HASH)` which was supposed to be provided by GLibC but RPM was not
detecting that it provided it.

Initially I thought maybe there was an RPM runtime dependency I did not have
causing RPM to not detect that GLibC provided it despite being able to detect
that other packages needed it. However after looking at the ‘Fedora 42’ RPM
spec file for their `glibc` package, what they do is hard-code it:

    Provides: rtld(GNU_HASH)

It bothers me a little bit that RPM will auto-detect a dependency it does not
have the ability to detect in the package that provides it, but it is what it
is I suppose.

Many of the spec files undoubtedly need work. Many undoubtedly have missing
`BuildRequires` and other packaging mistakes.


Duplicate Documentation
-----------------------

By default, LFS/BLFS does not compress man or info pages. By default, RPM uses
gzip compression on man and info pages. Thus when RPM bootstrapping an LFS
system, one typically ends up with two copies of each man and info page.

One solution is to gzip all man and info pages *before* the RPM bootstrap. That
way the files on the file system will have the same file name as the file names
in the RPM files. Similarly, one can configure the RPM build environment to NOT
gzip the man and info pages. Then once the bootstrap is complete, revert it to
gzip in future package builds. However, I just use a shell script to find and
delete the duplicates. Since RPM compresses them and the script only deletes the
uncompressed duplicates, it does not remove files under RPM management.

The shell script [`remove_duplicates.sh`](remove_duplicates.sh) can be used to
remove the duplicates. Run it once a day or so during the RPM bootstrap process,
definitely after installing RPM packaged Perl for the first time.


Bootstrap Build Order
---------------------

The build order is not *too* important. At the start, the `--nodeps` switch is
often needed because both library and runtime dependencies are in fact present
but not yet under RPM management, so the RPM database does not know about them.

I started with the [`kernel-abi-headers`](SPECS/kernel-abi-headers.spec) package
because it would be easy to restore that `noarch` package if something went
wrong, and I followed that with the [`vim`](SPECS/vim.spec) package because it
tested a binary build and again would be easy to restore the package if
something went wrong.

I deviated from the LFS instructions for the OpenSSL API stack, using LibreSSL
as my default library for the OpenSSL API and only using OpenSSL for Python
which does not support building against LibreSSL. To accomplish that in the LFS
build, LibreSSL was installed with a prefix of `/usr` and OpenSSL was installed
with a prefix of `/opt/openssl`.

With RPM management, both can be built with a prefix of `/usr` with the only
hitch being the `-devel` package for both can not be installed at the same time.

So next I rebuilt [`libressl`](SPECS/libressl.spec) followed by
[`openssl`](SPECS/openssl.spec) with a `/usr` prefix, allowing me to temporarily
uninstall the `libressl-devel` package so I could install the `openssl-devel`
package and rebuild [`python3`](SPECS/python3.spec) linking against OpenSSL
libraries in `/usr/lib` instead of in `/opt/openssl/lib` and the `/opt/openssl`
directory could be deleted.

The `openssl-devel` package was then uninstalled and `libressl-devel` restored
so that other packages that want the OpenSSL API and can link against LibreSSL
to get it would do so. I just *personally* have higher trust in the LibreSSL
developers and I do not care about FIPS certification.

LFS only builds `libelf` from ElfUtils but RPM requires `libdwarf` from ElfUtils
so part of building RPM itself was rebuilding ElfUtils *with* `libdwarf`. I thus
saw that as a deviation from LFS instructions, so next I built the full complete
[`elfutils`](SPECS/elfutils.spec) (using a `eu-` prefix on the binary
utilities which are not needed).

With GCC I deviated by bootstrapping it with Ada (`gnat`) and D (`gcd`) support,
I am working on a [`gcc`](SPECS/gcc.spec) RPM package that also builds all the
other languages (similar to the BLFS build of GCC). My GCC build also includes
the [Integer Set Library](https://en.wikipedia.org/wiki/Integer_set_library).
With GCC, ISL support can be added by unpacking the ISL source code into the
GCC source code and making sure the directory is named `isl` (as opposed to,
say, `isl-0.26`).

The [`gcc`](SPECS/gcc.spec) package now properly builds and is installed,
although I still need to add `m2` compiler support.

The only other major deviation from LFS is with the
[`make-ca`](SPECS/make-ca.spec) script which I patched to use the `libressl`
binary instead of the `openssl` binary, to use `curl` to retieve new
`certdata.txt` files, and to install with a default `certdata.txt` file so that
certificate bundles could be generated even if it is installed off-line.


Initial Bootstrap Order
-----------------------

With all of the major deviations packaged, the order followed is pretty much the
order in the LFS book starting with Chapter Five. I did not using the build
instructions from the early chapters of the LFS book as those were for creating
the build environment. Most of my build instructions were *fairly* similar to
the Chapter 8 build instructions.

After packaging [`util-linux`](util-linux) and thus completing the packages in
the LFS book through Chapter 7, I decided I needed a change in strategy.


Intermission Bootstrapping
--------------------------

* First, I needed git *inside* the LFS system being RPM bootstrapped to reduce
  how often a reboot is needed, so I built [`openssh`](SPECS/openssh.spec) and
  [`git`](SPECS/git.spec). Fortunately the spec files I had written for my LFS
  11.3 RPM system needed very little modification.
* Secondly, I decided it would be good to package [`gdb`](gdb.spec) and
  [`valgrind`](SPECS/valgrind.spec) now, so that package test suites that do
  more extensive testing when those packages are available can do that testing.
* Thirdly, I need to come up with a so-called ‘best practices’ for RPM spec
  files that I can use to audit my spec files.

Currently the first two are done, working on the third (in LaTeX, and not (yet)
in a public git)

Then I can go through the LFS book Chapter 8 in order, even rebuilding the
packages I already built so they have the benefit of gdb/valgrind in the test
suite and the spec file audit.

### Best Practices: RPM User and Group Dependency Notes

With new versions of RPM, if a specified file has user and/or group ownership
other than `root`, RPM will make the existence of that user and/or group a
package dependency.

Unfortunately RPM uses the facilities of `systemd-sysusers.d` to do so, even
though system users and groups being defined in the `/etc/passwd` and
`/etc/group` files are as old as UNIX itself, maybe even older?

With my `util-linux` package, RPM complained about needing `group(tty)` *even
though the group exists*. With my `openssh-server` package, RPM again complained
about needing `group(sys)` *even though the group exists*. This is just because
those groups are not defined in a systemd-sysusers unit file. In fact the *only*
systemd-sysusers file defined is for `dbus` which was installed from source
after SystemD was installed.

I probably will create the systemd-sysusers unit files for the standard system
users and groups *expected* to exist, however I do not like RPM requiring the
management of users and groups through systemd-sysusers so that is being turned
of via

    %_use_weak_usergroup_deps 1

in the `/etc/rpm/macros` file. That macro affects the *build* of a package,
packages built without that macro set to 1 will still have any non-root users
and groups defined in the `%files` section as package dependencies.

Note that with macro, the RPM will still *suggest* a user or group, it just will
not *require* the user or group.


LFS Chapter Eight Bootstrap
---------------------------

With the so-called ‘best practices’ developed and in hand, I will then package
everything in LFS 12.2 Chapter 8 either auditing existing RPM spec files to
bring them inline with the ‘best practices’ or writing brand new spec files
where I do not currently have them.

Going through the packages in the Chapter 8 order, any package that has build or
install dependencies RPM does not know about will have to have that dependency
packaged. For example, SQLite3 is not in the LFS book but when present, Python3
will use it to make a Python module for it, so when I get to Python3, I will
have to build an SQLite3 package if I have not already.

For the `man-pages` package, LFS packages it first because many of the man pages
in it get replaced by man pages from other packages. I am actually going to
change the install path to `/usr/share/generic-man` to avoid man page conflicts,
and put it at the *end* of the man path so that man pages from that collection
are only presented to the user if not provided by another package.

The rebuild of GCC in this phase is when I will add the `m2` (GNU Modula-2)
compiler support.

At this point, I will have a very good base and can go on to RPM bootstrapping
the various BLFS packages (and a few outside of BLF) and then finally build the
RPM package.
