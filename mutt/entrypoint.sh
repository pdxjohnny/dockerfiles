#!/usr/bin/env bash
# Set environment variable DEBUG=1 for debugging to /home/user/log
# Usage:
# docker run --name=mutt -ti -v $HOME/Documents/mutt:/home/user/muttv -e KUSER=$(keyring get intel idsid) -e KDOMAIN=AMR.CORP.INTEL.COM -e KPASSWORD=$(keyring get intel password) mutt

if [ ! -d "${HOME}/muttv" ]; then
  echo "Thou shalt mount \"${HOME}/muttv\" as a volume with 1000:1000 owner" 1>&2
  exit 1
fi

for i in $(ls -a ~/muttv | grep -v -w '..' | grep -v -w '.'); do
   ln -vs ~/muttv/$i ~/$i;
done

echo -e '[overrides]\ndefault-priority-string = NORMAL:+VERS-ALL:%COMPAT' > gnutls.ini

echo "${KPASSWORD}" | kinit "${KUSER}@${KDOMAIN}"

if [[ "x${DEBUG}" != "x" ]]; then
  export GNUTLS_SYSTEM_PRIORITY_FAIL_ON_INVALID=1
  export GNUTLS_SYSTEM_PRIORITY_FILE=gnutls.ini
  export GNUTLS_DEBUG_LEVEL=6
  export DEBUG="-v"
fi

mutt $DEBUG 2>log
