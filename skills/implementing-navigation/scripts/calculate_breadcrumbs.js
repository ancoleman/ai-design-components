#!/usr/bin/env node

/**
 * Calculate breadcrumb trails from navigation structure and current path.
 *
 * Usage:
 *   node calculate_breadcrumbs.js /products/category/item-123
 *   node calculate_breadcrumbs.js --config nav.json /products/category/item-123
 *   node calculate_breadcrumbs.js --format json /products/category/item-123
 */

const fs = require('fs');
const path = require('path');

/**
 * Default navigation structure if no config provided
 */
const DEFAULT_NAV = {
  items: [
    {
      label: 'Home',
      href: '/'
    },
    {
      label: 'Products',
      href: '/products',
      children: [
        {
          label: 'Electronics',
          href: '/products/electronics',
          children: [
            {
              label: 'Computers',
              href: '/products/electronics/computers'
            },
            {
              label: 'Phones',
              href: '/products/electronics/phones'
            }
          ]
        },
        {
          label: 'Clothing',
          href: '/products/clothing',
          children: [
            {
              label: 'Men',
              href: '/products/clothing/men'
            },
            {
              label: 'Women',
              href: '/products/clothing/women'
            }
          ]
        }
      ]
    },
    {
      label: 'About',
      href: '/about',
      children: [
        {
          label: 'Team',
          href: '/about/team'
        },
        {
          label: 'History',
          href: '/about/history'
        }
      ]
    },
    {
      label: 'Contact',
      href: '/contact'
    }
  ]
};

/**
 * Find navigation item by href
 */
function findItemByHref(items, href, parent = null) {
  for (const item of items) {
    if (item.href === href) {
      return { item, parent };
    }

    if (item.children) {
      const found = findItemByHref(item.children, href, item);
      if (found) return found;
    }
  }

  return null;
}

/**
 * Build breadcrumb trail from item to root
 */
function buildBreadcrumbTrail(navStructure, currentPath) {
  const trail = [];
  const { item, parent } = findItemByHref(navStructure.items, currentPath) || {};

  if (!item) {
    // Path not found in navigation, build from URL segments
    return buildBreadcrumbsFromPath(currentPath);
  }

  // Build trail from item to root
  let current = item;
  let currentParent = parent;

  trail.unshift({
    label: current.label,
    href: current.href,
    current: true
  });

  while (currentParent) {
    trail.unshift({
      label: currentParent.label,
      href: currentParent.href,
      current: false
    });

    // Find parent's parent
    const parentData = findParentItem(navStructure.items, currentParent);
    currentParent = parentData;
  }

  // Add home if not already there
  if (trail.length === 0 || trail[0].href !== '/') {
    trail.unshift({
      label: 'Home',
      href: '/',
      current: false
    });
  }

  return trail;
}

/**
 * Find parent of an item in navigation structure
 */
function findParentItem(items, targetItem, parent = null) {
  for (const item of items) {
    if (item === targetItem) {
      return parent;
    }

    if (item.children) {
      const found = findParentItem(item.children, targetItem, item);
      if (found !== undefined) return found;
    }
  }

  return undefined;
}

/**
 * Build breadcrumbs from URL path segments
 */
function buildBreadcrumbsFromPath(urlPath) {
  const segments = urlPath.split('/').filter(Boolean);
  const trail = [
    {
      label: 'Home',
      href: '/',
      current: urlPath === '/'
    }
  ];

  let currentPath = '';
  segments.forEach((segment, index) => {
    currentPath += '/' + segment;
    const label = segment
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');

    trail.push({
      label,
      href: currentPath,
      current: index === segments.length - 1
    });
  });

  return trail;
}

/**
 * Format breadcrumbs as HTML
 */
function formatAsHtml(breadcrumbs) {
  const items = breadcrumbs.map(crumb => {
    if (crumb.current) {
      return `    <li class="breadcrumb-item active" aria-current="page">${crumb.label}</li>`;
    } else {
      return `    <li class="breadcrumb-item"><a href="${crumb.href}">${crumb.label}</a></li>`;
    }
  }).join('\n');

  return `<nav aria-label="Breadcrumb">
  <ol class="breadcrumb">
${items}
  </ol>
</nav>`;
}

/**
 * Format breadcrumbs as React component
 */
function formatAsReact(breadcrumbs) {
  const items = breadcrumbs.map((crumb, index) => {
    if (crumb.current) {
      return `    <li key="${index}" className="breadcrumb-item active" aria-current="page">
      {${JSON.stringify(crumb.label)}}
    </li>`;
    } else {
      return `    <li key="${index}" className="breadcrumb-item">
      <Link to="${crumb.href}">${crumb.label}</Link>
    </li>`;
    }
  }).join('\n');

  return `<nav aria-label="Breadcrumb">
  <ol className="breadcrumb">
${items}
  </ol>
</nav>`;
}

/**
 * Format breadcrumbs as JSON-LD structured data
 */
function formatAsJsonLd(breadcrumbs) {
  const items = breadcrumbs.map((crumb, index) => ({
    "@type": "ListItem",
    "position": index + 1,
    "name": crumb.label,
    "item": crumb.current ? undefined : `https://example.com${crumb.href}`
  }));

  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": items
  };
}

/**
 * Format breadcrumbs as text
 */
function formatAsText(breadcrumbs, separator = ' > ') {
  return breadcrumbs.map(crumb => crumb.label).join(separator);
}

/**
 * Calculate breadcrumbs with smart matching
 */
function calculateSmartBreadcrumbs(navStructure, currentPath) {
  // Try exact match first
  let breadcrumbs = buildBreadcrumbTrail(navStructure, currentPath);

  // If not found, try parent paths
  if (breadcrumbs.length === 1 && currentPath !== '/') {
    const pathSegments = currentPath.split('/').filter(Boolean);

    for (let i = pathSegments.length - 1; i > 0; i--) {
      const parentPath = '/' + pathSegments.slice(0, i).join('/');
      const parentBreadcrumbs = buildBreadcrumbTrail(navStructure, parentPath);

      if (parentBreadcrumbs.length > 1) {
        // Found parent in navigation, add current page
        const currentLabel = pathSegments[pathSegments.length - 1]
          .split('-')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');

        parentBreadcrumbs[parentBreadcrumbs.length - 1].current = false;
        parentBreadcrumbs.push({
          label: currentLabel,
          href: currentPath,
          current: true
        });

        return parentBreadcrumbs;
      }
    }

    // Still not found, build from path
    breadcrumbs = buildBreadcrumbsFromPath(currentPath);
  }

  return breadcrumbs;
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  let configFile = null;
  let format = 'json';
  let currentPath = null;

  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' && i + 1 < args.length) {
      configFile = args[++i];
    } else if (args[i] === '--format' && i + 1 < args.length) {
      format = args[++i];
    } else if (!currentPath) {
      currentPath = args[i];
    }
  }

  if (!currentPath) {
    console.error('Usage: node calculate_breadcrumbs.js [--config nav.json] [--format json|html|react|jsonld|text] <current-path>');
    process.exit(1);
  }

  // Load navigation structure
  let navStructure = DEFAULT_NAV;
  if (configFile) {
    try {
      const data = fs.readFileSync(configFile, 'utf8');
      navStructure = JSON.parse(data);
    } catch (error) {
      console.error(`Error loading config: ${error.message}`);
      process.exit(1);
    }
  }

  // Calculate breadcrumbs
  const breadcrumbs = calculateSmartBreadcrumbs(navStructure, currentPath);

  // Output in requested format
  switch (format.toLowerCase()) {
    case 'html':
      console.log(formatAsHtml(breadcrumbs));
      break;

    case 'react':
      console.log(formatAsReact(breadcrumbs));
      break;

    case 'jsonld':
      console.log(JSON.stringify(formatAsJsonLd(breadcrumbs), null, 2));
      break;

    case 'text':
      console.log(formatAsText(breadcrumbs));
      break;

    case 'json':
    default:
      console.log(JSON.stringify(breadcrumbs, null, 2));
      break;
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

// Export for use as module
module.exports = {
  buildBreadcrumbTrail,
  buildBreadcrumbsFromPath,
  calculateSmartBreadcrumbs,
  formatAsHtml,
  formatAsReact,
  formatAsJsonLd,
  formatAsText
};