#!/bin/bash
set -e

echo "{}" > docs/manifests.json

if ls manifests/*.json 1> /dev/null 2>&1; then
  for file in manifests/*.json; do
    if [ -f "$file" ]; then
      filename=$(basename -- "$file")
      name=$(jq -r '.name // "Unknown App"' "$file")

      # Read the complete manifest content
      manifest_content=$(cat "$file")

      echo "Adding: $name ($filename)"
      jq --arg name "$name" --argjson content "$manifest_content" \
          '.[$name] = $content' \
          docs/manifests.json > docs/temp.json && mv docs/temp.json docs/manifests.json
    fi
  done
  echo "✅ Generated manifests.json with $(jq 'keys | length' docs/manifests.json) manifests"
else
  echo "No manifests found"
fi
