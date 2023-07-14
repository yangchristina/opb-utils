find . -iname 'questions/*/*.md' -type f -exec sed -i '' 's/[[:space:]]\{1,\}$//' {} \+
