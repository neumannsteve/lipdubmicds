#!/bin/sh

TEMPLATE=/usr/www/bin/template.pl
BASEDIR=/data/share/
INPDIR=www/hosted/lipdubmicds/
OUTDIR=test-www/lipdubmicds/
CGIPATH=${BASEDIR}${INPDIR}cgi-bin/

echo --- Generating Main Pages ---
${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -t:main-template.html -o -O:${OUTDIR} index.html

for sub in about signup ; do
  echo "${sub}..."
  ${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:${sub} -t:${sub}-template.html -o -O:${OUTDIR} -M "*.html"
done
