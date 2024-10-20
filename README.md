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

The shell script [`remove_duplicates.sh`](remove_duplicates.sh) can be used to
remove the duplicates. Run it once a day or so during the RPM bootstrap process,
definitely after installing RPM packaged Perl for the first time.
