import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  emoji: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Skillchain v2.1',
    emoji: '🔗',
    description: (
      <>
        Guided workflow system with blueprints, preferences, and phase-based
        development. Build full-stack applications with step-by-step guidance
        across frontend, backend, and infrastructure.
      </>
    ),
  },
  {
    title: 'Multi-Language Support',
    emoji: '🌐',
    description: (
      <>
        Production-ready skills for TypeScript, Python, Go, and Rust. Choose
        the right language for your project with comprehensive patterns and
        best practices for each ecosystem.
      </>
    ),
  },
  {
    title: 'Research-Backed',
    emoji: '🔬',
    description: (
      <>
        Every skill is validated with Google Search Grounding and Context7
        integration. Get up-to-date library recommendations with trust scores
        and working code examples.
      </>
    ),
  },
];

function Feature({title, emoji, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureEmoji}>{emoji}</div>
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Key Features
        </Heading>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
