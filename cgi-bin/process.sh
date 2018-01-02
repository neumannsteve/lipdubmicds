#!/bin/sh

TEMPLATE=/usr/www/bin/template.pl
BASEDIR=/usr/www/hosted/lipdubmicds/
INPDIR=staging/
OUTDIR=
CGIPATH=${BASEDIR}cgi-bin/

echo --- Generating Main Pages ---
${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -t:main-template.html -o -O:${OUTDIR} index.html

for sub in about signup ; do
  echo "${sub}..."
  ${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:${sub} -t:${sub}-template.html -o -O:${OUTDIR} -M "*.html"
done

echo --- Generating Blog Pages ---

cp -f ../staging/blog-theme/*.php ../blog-theme/
${TEMPLATE} -B:${BASEDIR} -I:${INPDIR} -C:blog-theme -t:blog-template.html -o -O:${OUTDIR} "index.php" "single.php" "page.php"
