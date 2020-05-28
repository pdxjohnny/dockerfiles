#!/usr/bin/env bash
# Usage:
# docker run --name=mutt -ti -v $HOME/Documents/mutt:/home/user/muttv -e KUSER=$(keyring get intel idsid) -e KDOMAIN=AMR.CORP.INTEL.COM -e KPASSWORD=$(keyring get intel password) mutt

if [ ! -d "${HOME}/muttv" ]; then
  echo "Thou shalt mount \"${HOME}/muttv\" as a volume with 1000:1000 owner" 1>&2
  exit 1
fi

for i in $(ls -a ~/muttv | grep -v -w '..' | grep -v -w '.'); do
   ln -vs ~/muttv/$i ~/$i;
done

echo -e '[overrides]\ndefault-priority-string = NORMAL:-VERS-ALL:+VERS-TLS1.1:+VERS-TLS1.0:+VERS-SSL3.0:%COMPAT' > gnutls.ini

printf "${KPASSWORD}" | kinit "${KUSER}@${KDOMAIN}"

GNUTLS_SYSTEM_PRIORITY_FAIL_ON_INVALID=1 GNUTLS_SYSTEM_PRIORITY_FILE=gnutls.ini GNUTLS_DEBUG_LEVEL=6 mutt 2>log
