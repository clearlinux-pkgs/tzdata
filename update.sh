#!/bin/bash

set -e
set -o pipefail

errexit() {
	local ret=1
	echo "Error: $1"
	if [[ -n "$2" ]]; then
		ret=2
	fi
	exit $ret
}

git pull --ff-only
BASE_URL="https://data.iana.org/time-zones/releases"

# Assumes no more than 26 releases in a given calendar year, which has been
# true to date. Also assumes 4 digits for representing the base version
# (calendar year).
TARS=$(mktemp)
trap "rm -f $TARS" EXIT
curl -sSf "$BASE_URL"/ | grep -Eo 'tz(code|data)[0-9]{4}[a-z]\.tar\.gz' | sort -ru > $TARS
if ! grep -q '^tzcode' $TARS; then
	errexit "no tzcode tarballs found"
fi
if ! grep -q '^tzdata' $TARS; then
	errexit "no tzdata tarballs found"
fi
CODE_VER=$(sed -n '/^tzcode/{s/^tzcode\([0-9]\{4\}[a-z]\).*/\1/p;q}' $TARS)
DATA_VER=$(sed -n '/^tzdata/{s/^tzdata\([0-9]\{4\}[a-z]\).*/\1/p;q}' $TARS)
if [[ -n "$CODE_VER" ]] && [[ "$CODE_VER" != "$DATA_VER" ]]; then
	errexit "code/data ver mismatch (code: \"$CODE_VER\"; data: \"$DATA_VER\")"
fi

CURRENT_VERSION="$(rpmspec --srpm -q --qf="%{VERSION}" tzdata.spec)"

if [[ "${CURRENT_VERSION}" = "${CODE_VER}" ]]; then
	errexit "already up-to-date ($CODE_VER is latest)" 2
fi

sed -e "s/##VERSION##/${CODE_VER}/g" tzdata.spec.in > tzdata.spec
make generateupstream || errexit "failed to generate upstream" 3

make bumpnogit
git add tzdata.spec Makefile release upstream
git commit -s -m "Update to ${CODE_VER}"
make koji
