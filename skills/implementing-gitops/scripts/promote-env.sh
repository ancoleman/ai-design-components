#!/bin/bash
# Promote image tag from one environment to another
set -e

SOURCE_ENV=${1}
TARGET_ENV=${2}

if [ -z "$SOURCE_ENV" ] || [ -z "$TARGET_ENV" ]; then
  echo "Usage: $0 <source-env> <target-env>"
  echo "Example: $0 dev staging"
  exit 1
fi

echo "Promoting from $SOURCE_ENV to $TARGET_ENV..."
echo ""

# This is a template script - customize for your repository structure
# Assumes kustomize overlays structure: k8s/overlays/{env}/

SOURCE_KUSTOMIZATION="k8s/overlays/$SOURCE_ENV/kustomization.yaml"
TARGET_KUSTOMIZATION="k8s/overlays/$TARGET_ENV/kustomization.yaml"

if [ ! -f "$SOURCE_KUSTOMIZATION" ]; then
  echo "Error: Source kustomization not found: $SOURCE_KUSTOMIZATION"
  exit 1
fi

if [ ! -f "$TARGET_KUSTOMIZATION" ]; then
  echo "Error: Target kustomization not found: $TARGET_KUSTOMIZATION"
  exit 1
fi

# Extract image tag from source environment
IMAGE_TAG=$(grep -A 2 "^images:" "$SOURCE_KUSTOMIZATION" | grep "newTag:" | awk '{print $2}')

if [ -z "$IMAGE_TAG" ]; then
  echo "Error: Could not extract image tag from $SOURCE_KUSTOMIZATION"
  exit 1
fi

echo "Found image tag: $IMAGE_TAG"
echo "Updating $TARGET_ENV to use this tag..."

# Update target environment kustomization
sed -i.bak "s/newTag:.*/newTag: $IMAGE_TAG/" "$TARGET_KUSTOMIZATION"

echo ""
echo "Promotion complete!"
echo ""
echo "Review changes:"
echo "  git diff $TARGET_KUSTOMIZATION"
echo ""
echo "Commit and push:"
echo "  git add $TARGET_KUSTOMIZATION"
echo "  git commit -m 'Promote $IMAGE_TAG from $SOURCE_ENV to $TARGET_ENV'"
echo "  git push"
