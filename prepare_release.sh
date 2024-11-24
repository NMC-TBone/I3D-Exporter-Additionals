#!/bin/bash

# Replace version number in blender_manifest.toml with the new version number. Can contain dev version.
sed -i "s/^version = \".*\"/version = \"$1\"/" $GITHUB_WORKSPACE/i3d_exporter_additionals/blender_manifest.toml

# Split the version tag into separate numbers for potential use (if needed)
IFS='.-' read -ra VERSION <<< "$1"

# Zip the addon directory into a new build
sudo apt-get install -y zip
cd $GITHUB_WORKSPACE
zip -r i3d_exporter_additionals.zip i3d_exporter_additionals
