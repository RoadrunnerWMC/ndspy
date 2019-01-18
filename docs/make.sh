# Command file for Sphinx documentation

: ${SPHINXBUILD:=sphinx-build}
SOURCEDIR="source"
BUILDDIR="build"
SPHINXPROJ="ndspy"

if [ -z "$1" ]; then
    $SPHINXBUILD -M help $SOURCEDIR $BUILDDIR $SPHINXOPTS
    exit 0
fi

# https://stackoverflow.com/a/677212
if ! hash $SPHINXBUILD 2>/dev/null; then
    echo ""
    echo "The 'sphinx-build' command was not found. Make sure you have Sphinx"
    echo "installed, then set the SPHINXBUILD environment variable to point"
    echo "to the full path of the 'sphinx-build' executable. Alternatively you"
    echo "may add the Sphinx directory to PATH."
    echo ""
    echo "If you don't have Sphinx installed, grab it from"
    echo "http://sphinx-doc.org/"
    exit 1
fi

$SPHINXBUILD -M $1 $SOURCEDIR $BUILDDIR $SPHINXOPTS
