import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <img
          src="/ai-design-components/img/logo.png"
          alt="AI Design Components"
          className={styles.heroLogo}
        />
        <p className={styles.heroTagline}>Claude Skills for Full-Stack Development</p>
        <p className={styles.heroSubtitle}>
          76 skills covering UI/UX, Backend, DevOps, Security, Cloud, and AI/ML
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Get Started
          </Link>
          <Link
            className="button button--secondary button--lg"
            href="https://github.com/ancoleman/ai-design-components">
            View on GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

function StatsSection() {
  const stats = [
    { value: '76', label: 'Production Skills' },
    { value: '18', label: 'Plugin Groups' },
    { value: '4', label: 'Languages' },
    { value: '3', label: 'Blueprints' },
  ];

  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className={styles.statsGrid}>
          {stats.map((stat, idx) => (
            <div key={idx} className={styles.statCard}>
              <div className={styles.statValue}>{stat.value}</div>
              <div className={styles.statLabel}>{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function QuickLinksSection() {
  const links = [
    {
      title: 'Skills Directory',
      description: 'Explore all 76 production-ready skills across frontend, backend, DevOps, and more',
      to: '/docs/skills/overview',
    },
    {
      title: 'Skillchain Guide',
      description: 'Learn how to use the guided workflow system with blueprints',
      to: '/docs/skillchain/overview',
    },
    {
      title: 'Installation',
      description: 'Get started with AI Design Components in your projects',
      to: '/docs/installation',
    },
  ];

  return (
    <section className={styles.quickLinksSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Quick Links
        </Heading>
        <div className={styles.quickLinksGrid}>
          {links.map((link, idx) => (
            <Link key={idx} to={link.to} className={styles.quickLinkCard}>
              <Heading as="h3">{link.title}</Heading>
              <p>{link.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="Claude Skills for Full-Stack Development - 76 skills covering UI/UX, Backend, DevOps, Security, Cloud, and AI/ML">
      <HomepageHeader />
      <main>
        <StatsSection />
        <HomepageFeatures />
        <QuickLinksSection />
      </main>
    </Layout>
  );
}
