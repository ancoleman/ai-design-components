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
        'guides/skill-validation',
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
        'skills/backend/implementing-api-patterns',
        'skills/backend/using-relational-databases',
        'skills/backend/using-vector-databases',
        'skills/backend/using-timeseries-databases',
        'skills/backend/using-document-databases',
        'skills/backend/using-graph-databases',
        'skills/backend/using-message-queues',
        'skills/backend/implementing-realtime-sync',
        'skills/backend/implementing-observability',
        'skills/backend/securing-authentication',
        'skills/backend/ai-data-engineering',
        'skills/backend/model-serving',
        'skills/backend/deploying-applications',
        'skills/backend/ingesting-data',
      ],
    },
    {
      type: 'category',
      label: 'DevOps Skills',
      link: {
        type: 'generated-index',
        description: 'DevOps, CI/CD, and platform engineering skills',
      },
      items: [
        'skills/devops/testing-strategies',
        'skills/devops/building-ci-pipelines',
        'skills/devops/implementing-gitops',
        'skills/devops/platform-engineering',
        'skills/devops/managing-incidents',
        'skills/devops/writing-dockerfiles',
      ],
    },
    {
      type: 'category',
      label: 'Infrastructure Skills',
      link: {
        type: 'generated-index',
        description: 'Infrastructure, networking, and platform operations skills',
      },
      items: [
        'skills/infrastructure/operating-kubernetes',
        'skills/infrastructure/writing-infrastructure-code',
        'skills/infrastructure/administering-linux',
        'skills/infrastructure/architecting-networks',
        'skills/infrastructure/load-balancing-patterns',
        'skills/infrastructure/planning-disaster-recovery',
        'skills/infrastructure/configuring-nginx',
        'skills/infrastructure/shell-scripting',
        'skills/infrastructure/managing-dns',
        'skills/infrastructure/implementing-service-mesh',
        'skills/infrastructure/managing-configuration',
        'skills/infrastructure/designing-distributed-systems',
      ],
    },
    {
      type: 'category',
      label: 'Security Skills',
      link: {
        type: 'generated-index',
        description: 'Security, compliance, and vulnerability management skills',
      },
      items: [
        'skills/security/architecting-security',
        'skills/security/implementing-compliance',
        'skills/security/managing-vulnerabilities',
        'skills/security/implementing-tls',
        'skills/security/configuring-firewalls',
        'skills/security/siem-logging',
        'skills/security/security-hardening',
      ],
    },
    {
      type: 'category',
      label: 'Developer Productivity Skills',
      link: {
        type: 'generated-index',
        description: 'Developer tools, workflows, and productivity skills',
      },
      items: [
        'skills/developer-productivity/designing-apis',
        'skills/developer-productivity/building-clis',
        'skills/developer-productivity/designing-sdks',
        'skills/developer-productivity/generating-documentation',
        'skills/developer-productivity/debugging-techniques',
        'skills/developer-productivity/managing-git-workflows',
        'skills/developer-productivity/writing-github-actions',
      ],
    },
    {
      type: 'category',
      label: 'Data Engineering Skills',
      link: {
        type: 'generated-index',
        description: 'Data architecture, streaming, and performance optimization skills',
      },
      items: [
        'skills/data-engineering/architecting-data',
        'skills/data-engineering/streaming-data',
        'skills/data-engineering/transforming-data',
        'skills/data-engineering/optimizing-sql',
        'skills/data-engineering/secret-management',
        'skills/data-engineering/performance-engineering',
      ],
    },
    {
      type: 'category',
      label: 'AI/ML Skills',
      link: {
        type: 'generated-index',
        description: 'AI/ML operations, prompt engineering, and model optimization skills',
      },
      items: [
        'skills/ai-ml/implementing-mlops',
        'skills/ai-ml/prompt-engineering',
        'skills/ai-ml/evaluating-llms',
        'skills/ai-ml/embedding-optimization',
      ],
    },
    {
      type: 'category',
      label: 'Cloud Skills',
      link: {
        type: 'generated-index',
        description: 'Cloud platform deployment and management skills',
      },
      items: [
        'skills/cloud/deploying-on-aws',
        'skills/cloud/deploying-on-gcp',
        'skills/cloud/deploying-on-azure',
      ],
    },
    {
      type: 'category',
      label: 'FinOps Skills',
      link: {
        type: 'generated-index',
        description: 'Financial operations, cost optimization, and resource management skills',
      },
      items: [
        'skills/finops/optimizing-costs',
        'skills/finops/resource-tagging',
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
        'master-plans/infrastructure/operating-kubernetes',
        'master-plans/infrastructure/writing-infrastructure-code',
        'master-plans/infrastructure/administering-linux',
        'master-plans/infrastructure/architecting-networks',
        'master-plans/infrastructure/load-balancing-patterns',
        'master-plans/infrastructure/planning-disaster-recovery',
        'master-plans/infrastructure/configuring-nginx',
        'master-plans/infrastructure/shell-scripting',
        'master-plans/infrastructure/managing-dns',
        'master-plans/infrastructure/implementing-service-mesh',
        'master-plans/infrastructure/managing-configuration',
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
        'master-plans/security/architecting-security',
        'master-plans/security/implementing-compliance',
        'master-plans/security/managing-vulnerabilities',
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
        'master-plans/devops/implementing-gitops',
        'master-plans/devops/testing-strategies',
        'master-plans/devops/platform-engineering',
        'master-plans/devops/managing-incidents',
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
        'master-plans/developer-productivity/designing-apis',
        'master-plans/developer-productivity/building-clis',
        'master-plans/developer-productivity/designing-sdks',
        'master-plans/developer-productivity/generating-documentation',
        'master-plans/developer-productivity/debugging-techniques',
        'master-plans/developer-productivity/managing-git-workflows',
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
        'master-plans/data/architecting-data',
        'master-plans/data/streaming-data',
        'master-plans/data/transforming-data',
        'master-plans/data/optimizing-sql',
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
        'master-plans/ai-ml/implementing-mlops',
        'master-plans/ai-ml/prompt-engineering',
        'master-plans/ai-ml/evaluating-llms',
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
        'master-plans/cloud/deploying-on-aws',
        'master-plans/cloud/deploying-on-gcp',
        'master-plans/cloud/deploying-on-azure',
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
        'master-plans/finops/optimizing-costs',
        'master-plans/finops/resource-tagging',
        'master-plans/finops/security-hardening',
      ],
    },
  ],
};

export default sidebars;
