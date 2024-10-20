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

The Perl spec file builds packages but needs to be split up into lots of smaller
packages. For RPM bootstrapping, that does not matter. That is a lot of tedious
work but the value is a small bug fix in a bundled module can then be updated
via RPM without needing to rebuild all of Perl.

The GLibC spec file has a bug. Other packages detect they need `rtld(GNU_HASH)`
which I believe is provided by GLibC but the packaging of GLibC does not detect
that it provides it. I could auto-specify that it provides it, but part of me
wonders if there actually is a runtime dependency for RPM missing that prevents
RPM from automatically picking up that GLibC as compiled?

Yes, `binutils` is compiled with `--enable-default-hash-style=gnu` and clearly
it is working as RPM detects `rtld(GNU_HASH)` as a needed dependency, but for
whatever reason, the RPM build of GLibC does not auto-detect that GLibC is
providing it.

Many of the spec files undoubtedly need work. Many undoubtedly have missing
`BuildRequires` and other packaging mistakes.


Duplicate Documentation
-----------------------

By default, LFS/BLFS does not compress man or info pages. By default, RPM uses
gzip compression on man and info pages. Thus when RPM bootstrapping an LFS
system, you will likely end up with two copies of each man and info page.

One solution is to gzip all man and info pages *before* the RPM bootstrap. That
way the files on the file system will have the same file name as the file names
in the RPM files. Similarly, you can configure your RPM build environment to NOT
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
as my default library for the OpenSSL API stack and only using OpenSSL for
Python which does not support building against LibreSSL. To accomplish that in
the LFS build, LibreSSL was installed with a prefix of `/usr` and OpenSSL was
installed with a prefix of `/opt/openssl`.

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
utilities).

With GCC I deviated by bootstrapping it with Ada (`gnat`) and D (`gcd`) support,
I am working on a [`gcc`](SPECS/gcc.spec) RPM package that also builds all the
other languages (similar to the BLFS build of GCC). My GCC build also includes
the [Integer Set Library](https://en.wikipedia.org/wiki/Integer_set_library).
With GCC, ISL support can be added by unpacking the ISL source code into the
GCC source code and making sure the directory is named `isl` (as opposed to,
say, `isl-0.26`).

The only other major deviation from LFS is with the `make-ca` script that is
technically from BLFS but that package is shell script only and I will likely
wait until after SystemD is RPM bootstrapped since it uses a SystemD timer unit
to run once a week.

With all of the major deviations packaged *except* GCC (being worked on) and
`make-ca` (waiting until after SystemD is packaged), the order I am following is
pretty much the order in the LFS book starting with Chapter Five. I am not
using the build instructions from the early chapters of the LFS book, most of my
build instructions are *fairly* similar to the Chapter 8 build instructions.

Once GCC is finished and Util-Linux (not yet started) is finished, the plan is
to pause and audit each spec file, making sure things like the specified license
is correct and other things, before proceeding with RPM bootstrapping the
packages in Chapter 8 that are not already RPM packaged.

I may have to do the kernel sooner as there are some kernel options I should
have enabled but did not. My intent is for RPM itself to be the very *last*
package I RPM bootstrap before going on to the next phase (building `dnf` and
`mock`).
