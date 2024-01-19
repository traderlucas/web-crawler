TAP_VERSION=$(python setup.py --version)

next_tap_version=$(echo "$TAP_VERSION" | awk 'BEGIN { FS="." } { $3++} { printf "%d.%d.%d\n", $1, $2, $3 }')
param=s/version=.*/version="\"${next_tap_version}\","/

sed -i "$param" setup.py

git add setup.py
git commit -m "[skip CI]"
git push 
git tag -m 'Bumped version through bitbucket pipelines' $next_tap_version
git push origin $next_tap_version
