if [ $# -eq 1 ]; then
    git add .
    git commit -m "$1"
    git push origin
else
    echo "Pass just one parameter: it will be the commit's comment"
fi
