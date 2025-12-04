import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Main documentation sidebar
  tutorialSidebar: [
    'intro',
    'installation',
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/creating-skills',
        'guides/research-methodology',
        'guides/best-practices',
        'guides/llm-ecosystem',
      ],
    },
  ],

  // Skills documentation
  skillsSidebar: [
    'skills/overview',
    {
      type: 'category',
      label: 'Frontend Skills',
      link: {
        type: 'generated-index',
        description: 'UI/UX component design and implementation skills',
      },
      items: [
        'skills/frontend/theming-components',
        'skills/frontend/visualizing-data',
        'skills/frontend/building-forms',
        'skills/frontend/building-tables',
        'skills/frontend/creating-dashboards',
        'skills/frontend/providing-feedback',
        'skills/frontend/implementing-navigation',
        'skills/frontend/implementing-search-filter',
        'skills/frontend/designing-layouts',
        'skills/frontend/managing-media',
        'skills/frontend/displaying-timelines',
        'skills/frontend/implementing-drag-drop',
        'skills/frontend/guiding-users',
        'skills/frontend/building-ai-chat',
        'skills/frontend/assembling-components',
      ],
    },
    {
      type: 'category',
      label: 'Backend Skills',
      link: {
        type: 'generated-index',
        description: 'Server-side, database, and infrastructure skills',
      },
      items: [
        'skills/backend/api-patterns',
        'skills/backend/databases-relational',
        'skills/backend/databases-vector',
        'skills/backend/databases-timeseries',
        'skills/backend/databases-document',
        'skills/backend/databases-graph',
        'skills/backend/message-queues',
        'skills/backend/realtime-sync',
        'skills/backend/observability',
        'skills/backend/auth-security',
        'skills/backend/ai-data-engineering',
        'skills/backend/model-serving',
        'skills/backend/deploying-applications',
        'skills/backend/ingesting-data',
      ],
    },
  ],

  // Skillchain documentation
  skillchainSidebar: [
    'skillchain/overview',
    'skillchain/installation',
    'skillchain/usage',
    'skillchain/blueprints',
    'skillchain/architecture',
  ],

  // Master plans sidebar
  masterPlansSidebar: [
    'master-plans/overview',
    {
      type: 'category',
      label: 'Infrastructure',
      link: {
        type: 'generated-index',
        description: 'Infrastructure and platform skill master plans',
      },
      items: [
        'master-plans/infrastructure/kubernetes-operations',
        'master-plans/infrastructure/infrastructure-as-code',
        'master-plans/infrastructure/linux-administration',
        'master-plans/infrastructure/network-architecture',
        'master-plans/infrastructure/load-balancing-patterns',
        'master-plans/infrastructure/disaster-recovery',
        'master-plans/infrastructure/configuring-nginx',
        'master-plans/infrastructure/shell-scripting',
        'master-plans/infrastructure/dns-management',
        'master-plans/infrastructure/service-mesh',
        'master-plans/infrastructure/configuration-management',
        'master-plans/infrastructure/designing-distributed-systems',
      ],
    },
    {
      type: 'category',
      label: 'Security',
      link: {
        type: 'generated-index',
        description: 'Security and compliance skill master plans',
      },
      items: [
        'master-plans/security/security-architecture',
        'master-plans/security/compliance-frameworks',
        'master-plans/security/vulnerability-management',
        'master-plans/security/implementing-tls',
        'master-plans/security/configuring-firewalls',
        'master-plans/security/siem-logging',
      ],
    },
    {
      type: 'category',
      label: 'DevOps',
      link: {
        type: 'generated-index',
        description: 'DevOps and CI/CD skill master plans',
      },
      items: [
        'master-plans/devops/building-ci-pipelines',
        'master-plans/devops/gitops-workflows',
        'master-plans/devops/testing-strategies',
        'master-plans/devops/platform-engineering',
        'master-plans/devops/incident-management',
        'master-plans/devops/writing-dockerfiles',
      ],
    },
    {
      type: 'category',
      label: 'Developer Productivity',
      link: {
        type: 'generated-index',
        description: 'Developer tools and workflow skill master plans',
      },
      items: [
        'master-plans/developer-productivity/api-design-principles',
        'master-plans/developer-productivity/building-clis',
        'master-plans/developer-productivity/sdk-design',
        'master-plans/developer-productivity/documentation-generation',
        'master-plans/developer-productivity/debugging-techniques',
        'master-plans/developer-productivity/git-workflows',
        'master-plans/developer-productivity/writing-github-actions',
      ],
    },
    {
      type: 'category',
      label: 'Data Engineering',
      link: {
        type: 'generated-index',
        description: 'Data engineering and analytics skill master plans',
      },
      items: [
        'master-plans/data/data-architecture',
        'master-plans/data/streaming-data',
        'master-plans/data/data-transformation',
        'master-plans/data/sql-optimization',
        'master-plans/data/secret-management',
        'master-plans/data/performance-engineering',
      ],
    },
    {
      type: 'category',
      label: 'AI & Machine Learning',
      link: {
        type: 'generated-index',
        description: 'AI/ML operations and optimization skill master plans',
      },
      items: [
        'master-plans/ai-ml/mlops-patterns',
        'master-plans/ai-ml/prompt-engineering',
        'master-plans/ai-ml/llm-evaluation',
        'master-plans/ai-ml/embedding-optimization',
      ],
    },
    {
      type: 'category',
      label: 'Cloud',
      link: {
        type: 'generated-index',
        description: 'Cloud platform skill master plans',
      },
      items: [
        'master-plans/cloud/aws-patterns',
        'master-plans/cloud/gcp-patterns',
        'master-plans/cloud/azure-patterns',
      ],
    },
    {
      type: 'category',
      label: 'FinOps',
      link: {
        type: 'generated-index',
        description: 'Financial operations and cost management skill master plans',
      },
      items: [
        'master-plans/finops/cost-optimization',
        'master-plans/finops/resource-tagging',
        'master-plans/finops/security-hardening',
      ],
    },
  ],
};

export default sidebars;
