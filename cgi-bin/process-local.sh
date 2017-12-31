#!/bin/sh

TEMPLATE=/usr/www/bin/template.pl
BASEDIR=/data/share/
INPDIR=www/hosted/lipdubmicds/
OUTDIR=test-www/lipdubmicds/
CGIPATH=${BASEDIR}${INPDIR}cgi-bin/

echo --- Generating Main Pages ---
${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -t:main-template.html -o -O:${OUTDIR} index.html

#for sub in about web print photography apps contact test eblast ; do
#  echo "${sub}..."
#  ${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:${sub} -t:${sub}-template.html -o -O:${OUTDIR} -M -f:notracking=true "*.html"
#  for subsub in `find ${BASEDIR}${INPDIR}${sub} -type d -depth 1 -print | grep -v images | grep -v '.svn' | grep -v '${sub}/$$' | xargs -L 1 basename` ; do
#    echo "    ${subsub}..."
#    ${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:${sub}/${subsub} -t:${sub}-template.html -o -O:${OUTDIR} -M -f:notracking=true "*.html"
#    for subsubsub in `find ${BASEDIR}${INPDIR}${sub}/${subsub} -type d -depth 1 -print | grep -v images | grep -v '.svn' | grep -v '${sub}/{$subsub}/$$' | grep -v css | grep -v js | grep -v development-bundle | xargs -L 1 basename` ; do
#      echo "      ${subsubsub}..."
#      ${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:${sub}/${subsub}/${subsubsub} -t:${sub}-template.html -o -O:${OUTDIR} -M -f:notracking=true "*.html"
#    done
#  done
#done
