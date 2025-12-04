import React from 'react';
import BlogLayout from '@theme-original/BlogLayout';
import type BlogLayoutType from '@theme/BlogLayout';
import type {WrapperProps} from '@docusaurus/types';
import styles from './styles.module.css';

type Props = WrapperProps<typeof BlogLayoutType>;

export default function BlogLayoutWrapper(props: Props): JSX.Element {
  return (
    <>
      <div className={styles.blogHeader}>
        <div className={styles.blogHeaderContent}>
          <img
            src="/ai-design-components/img/logo.png"
            alt="AI Design Components"
            className={styles.blogLogo}
          />
          <p className={styles.blogTagline}>
            Updates, releases, and insights about AI Design Components
          </p>
        </div>
      </div>
      <BlogLayout {...props} />
    </>
  );
}
