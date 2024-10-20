#!/bin/bash

if [ "`whoami`" != "root" ]; then
  echo "You must run this as r00t. Sorry."
  exit 1
fi

pushd /usr/share/man
for file in `find . -type f -print`; do
  if [ -f "${file}.gz" ]; then
    echo "removing ${file} as duplicate"
    rm -f ${file}
    sleep 0.3
  fi
done
popd
pushd /usr/share/info
for file in `find . -type f -print`; do
  if [ -f "${file}.gz" ]; then
    echo "removing ${file} as duplicate"
    rm -f ${file}
    sleep 0.3
  fi
done
popd
