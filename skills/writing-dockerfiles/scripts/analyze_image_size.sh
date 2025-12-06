#!/bin/bash
#
# Docker Image Size Analysis Script
#
# Compares image sizes before and after optimization.
# Shows layer-by-layer breakdown and size differences.
#
# Usage:
#   ./analyze_image_size.sh image:tag
#   ./analyze_image_size.sh image:before image:after

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to format bytes to human-readable
format_bytes() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.1f\", $bytes/1024}")KB"
    elif [ $bytes -lt 1073741824 ]; then
        echo "$(awk "BEGIN {printf \"%.1f\", $bytes/1048576}")MB"
    else
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1073741824}")GB"
    fi
}

# Function to analyze single image
analyze_image() {
    local image=$1
    echo -e "${BLUE}=== Analyzing: $image ===${NC}\n"

    # Check if image exists
    if ! docker image inspect "$image" &>/dev/null; then
        echo -e "${RED}Error: Image '$image' not found${NC}"
        return 1
    fi

    # Get image size
    local size=$(docker image inspect "$image" --format='{{.Size}}')
    local size_hr=$(format_bytes $size)

    echo -e "${GREEN}Total Size:${NC} $size_hr ($size bytes)"

    # Get layer count
    local layers=$(docker history "$image" --no-trunc --format='{{.ID}}' | wc -l)
    echo -e "${GREEN}Layer Count:${NC} $layers"

    # Show layer breakdown
    echo -e "\n${YELLOW}Layer Breakdown:${NC}"
    docker history "$image" --human --no-trunc --format='table {{.Size}}\t{{.CreatedBy}}' | head -n 20

    # Get base image if FROM instruction found
    local base=$(docker history "$image" --human --no-trunc | tail -n 1 | awk '{print $1}')
    if [ "$base" != "<missing>" ]; then
        echo -e "\n${GREEN}Base Image Size:${NC} $base"
    fi

    echo ""
}

# Function to compare two images
compare_images() {
    local image1=$1
    local image2=$2

    echo -e "${BLUE}=== Comparing Images ===${NC}\n"

    # Get sizes
    local size1=$(docker image inspect "$image1" --format='{{.Size}}')
    local size2=$(docker image inspect "$image2" --format='{{.Size}}')

    local size1_hr=$(format_bytes $size1)
    local size2_hr=$(format_bytes $size2)

    echo -e "${YELLOW}Image 1:${NC} $image1"
    echo -e "${GREEN}Size:${NC} $size1_hr ($size1 bytes)"

    echo ""

    echo -e "${YELLOW}Image 2:${NC} $image2"
    echo -e "${GREEN}Size:${NC} $size2_hr ($size2 bytes)"

    echo ""

    # Calculate difference
    local diff=$(($size2 - $size1))
    local diff_hr=$(format_bytes ${diff#-})  # Remove negative sign for formatting
    local diff_pct=$(awk "BEGIN {printf \"%.1f\", ($diff / $size1) * 100}")

    if [ $diff -lt 0 ]; then
        echo -e "${GREEN}Size Reduction:${NC} $diff_hr (${diff_pct#-}% smaller)"
    elif [ $diff -gt 0 ]; then
        echo -e "${RED}Size Increase:${NC} $diff_hr (${diff_pct}% larger)"
    else
        echo -e "${YELLOW}Same Size${NC}"
    fi

    echo ""
}

# Main script
if [ $# -eq 1 ]; then
    # Single image analysis
    analyze_image "$1"
elif [ $# -eq 2 ]; then
    # Compare two images
    if ! docker image inspect "$1" &>/dev/null; then
        echo -e "${RED}Error: Image '$1' not found${NC}"
        exit 1
    fi
    if ! docker image inspect "$2" &>/dev/null; then
        echo -e "${RED}Error: Image '$2' not found${NC}"
        exit 1
    fi

    analyze_image "$1"
    echo ""
    analyze_image "$2"
    echo ""
    compare_images "$1" "$2"
else
    echo "Usage:"
    echo "  $0 image:tag                  # Analyze single image"
    echo "  $0 image:before image:after   # Compare two images"
    echo ""
    echo "Examples:"
    echo "  $0 myapp:latest"
    echo "  $0 myapp:before myapp:after"
    exit 1
fi
