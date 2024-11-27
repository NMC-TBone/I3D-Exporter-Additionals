#!/bin/bash

# Replace version number in blender_manifest.toml with the new version number. Can contain dev version.
sed -i "s/^version = \".*\"/version = \"$1\"/" $GITHUB_WORKSPACE/i3d_exporter_additionals/blender_manifest.toml

# Create a versioned zip file
cd $GITHUB_WORKSPACE
zip -r "i3d_exporter_additionals-$1.zip" i3d_exporter_additionals

echo "Zip file created: i3d_exporter_additionals-$1.zip"
ls -la
