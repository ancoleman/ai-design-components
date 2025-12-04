import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'AI Design Components',
  tagline: 'Claude Skills for Full-Stack Development',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://ancoleman.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-design-components/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'ancoleman', // Usually your GitHub org/user name.
  projectName: 'ai-design-components', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/ancoleman/ai-design-components/tree/main/pages/',
        },
        blog: {
          showReadingTime: true,
          blogSidebarCount: 'ALL',
          blogSidebarTitle: 'All Posts',
          feedOptions: {
            type: 'all',
            copyright: `Copyright © ${new Date().getFullYear()} AI Design Components`,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/ancoleman/ai-design-components/tree/main/pages/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'AI Design Components',
      logo: {
        alt: 'AI Design Components Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          type: 'docSidebar',
          sidebarId: 'skillsSidebar',
          position: 'left',
          label: 'Skills',
        },
        {
          type: 'docSidebar',
          sidebarId: 'skillchainSidebar',
          position: 'left',
          label: 'Skillchain',
        },
        {
          type: 'docSidebar',
          sidebarId: 'masterPlansSidebar',
          position: 'left',
          label: 'Master Plans',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          to: '/llm-ecosystem',
          label: 'LLM Ecosystem',
          position: 'right',
        },
        {
          href: 'https://github.com/ancoleman/ai-design-components',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Installation',
              to: '/docs/installation',
            },
            {
              label: 'Skills',
              to: '/docs/skills/overview',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Skillchain',
              to: '/docs/skillchain/overview',
            },
            {
              label: 'Master Plans',
              to: '/docs/master-plans/overview',
            },
            {
              label: 'Guides',
              to: '/docs/guides/creating-skills',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/ancoleman/ai-design-components',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI Design Components. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
