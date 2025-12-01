/**
 * Skill Library Visualization Demo
 *
 * Showcases three different visualization approaches for the same dataset:
 * 1. Treemap - Hierarchical overview (best for at-a-glance understanding)
 * 2. Grouped Bar Chart - Category comparison (best for progress tracking)
 * 3. Sunburst Chart - Interactive exploration (best for engagement)
 *
 * Demonstrates data-viz skill guidance on selecting appropriate chart types
 * based on data characteristics and analytical purpose.
 */

import React, { useState } from 'react';
import { SkillLibraryTreemap } from './SkillLibraryTreemap';
import { SkillLibraryBarChart } from './SkillLibraryBarChart';
import { SkillLibrarySunburst } from './SkillLibrarySunburst';
import { skillLibraryStats } from './skillLibraryData';

type VisualizationType = 'treemap' | 'barchart' | 'sunburst' | 'all';

export default function App() {
  const [activeView, setActiveView] = useState<VisualizationType>('all');

  const visualizations = [
    {
      id: 'treemap' as const,
      name: 'Treemap',
      description: 'Hierarchical Overview',
      icon: '🔲',
      bestFor: 'At-a-glance understanding of structure and status',
      component: <SkillLibraryTreemap />
    },
    {
      id: 'barchart' as const,
      name: 'Grouped Bar Chart',
      description: 'Plugin Group Comparison',
      icon: '📊',
      bestFor: 'Comparing progress across plugin groups',
      component: <SkillLibraryBarChart />
    },
    {
      id: 'sunburst' as const,
      name: 'Sunburst Chart',
      description: 'Interactive Exploration',
      icon: '☀️',
      bestFor: 'Engaging interactive hierarchy exploration',
      component: <SkillLibrarySunburst />
    }
  ];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', padding: '24px' }}>
      {/* Header */}
      <header style={{ maxWidth: '1400px', margin: '0 auto 32px' }}>
        <h1 style={{ margin: 0, fontSize: '36px', fontWeight: 'bold', color: '#111' }}>
          AI Design Components - Skill Library Visualizations
        </h1>
        <p style={{ margin: '12px 0', fontSize: '18px', color: '#666' }}>
          Three complementary views of the same data using the data-viz skill
        </p>

        {/* Stats banner */}
        <div
          style={{
            marginTop: '16px',
            padding: '16px',
            backgroundColor: '#fff',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px'
          }}
        >
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#228833' }}>
              {skillLibraryStats.completeSkills}
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>Complete Skills</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFB000' }}>
              {skillLibraryStats.wipSkills}
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>In Progress</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#4477AA' }}>
              {skillLibraryStats.totalPluginGroups}
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>Plugin Groups</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#111' }}>
              {Math.round(skillLibraryStats.completionRate * 100)}%
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>Overall Progress</div>
          </div>
        </div>
      </header>

      {/* View selector */}
      <nav
        style={{
          maxWidth: '1400px',
          margin: '0 auto 32px',
          display: 'flex',
          gap: '12px',
          flexWrap: 'wrap'
        }}
        role="tablist"
      >
        <button
          onClick={() => setActiveView('all')}
          style={{
            padding: '12px 20px',
            fontSize: '16px',
            fontWeight: activeView === 'all' ? 'bold' : 'normal',
            backgroundColor: activeView === 'all' ? '#2196f3' : '#fff',
            color: activeView === 'all' ? '#fff' : '#111',
            border: activeView === 'all' ? 'none' : '2px solid #e0e0e0',
            borderRadius: '6px',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
          role="tab"
          aria-selected={activeView === 'all'}
        >
          🎨 All Views
        </button>
        {visualizations.map(viz => (
          <button
            key={viz.id}
            onClick={() => setActiveView(viz.id)}
            style={{
              padding: '12px 20px',
              fontSize: '16px',
              fontWeight: activeView === viz.id ? 'bold' : 'normal',
              backgroundColor: activeView === viz.id ? '#2196f3' : '#fff',
              color: activeView === viz.id ? '#fff' : '#111',
              border: activeView === viz.id ? 'none' : '2px solid #e0e0e0',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            role="tab"
            aria-selected={activeView === viz.id}
          >
            {viz.icon} {viz.name}
          </button>
        ))}
      </nav>

      {/* Visualization selection guide (shown in 'all' view) */}
      {activeView === 'all' && (
        <div
          style={{
            maxWidth: '1400px',
            margin: '0 auto 32px',
            padding: '20px',
            backgroundColor: '#fff3cd',
            border: '2px solid #ffc107',
            borderRadius: '8px'
          }}
        >
          <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: 'bold' }}>
            📚 Choosing the Right Visualization
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px', fontSize: '14px' }}>
            {visualizations.map(viz => (
              <div key={viz.id} style={{ padding: '12px', backgroundColor: 'rgba(255,255,255,0.6)', borderRadius: '4px' }}>
                <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                  {viz.icon} {viz.name}
                </div>
                <div style={{ color: '#666' }}>
                  <strong>Best for:</strong> {viz.bestFor}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main content area */}
      <main
        style={{
          maxWidth: '1400px',
          margin: '0 auto'
        }}
      >
        {activeView === 'all' ? (
          <div style={{ display: 'grid', gap: '32px' }}>
            {visualizations.map(viz => (
              <section
                key={viz.id}
                style={{
                  padding: '24px',
                  backgroundColor: '#fff',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
              >
                {viz.component}
              </section>
            ))}
          </div>
        ) : (
          <section
            style={{
              padding: '24px',
              backgroundColor: '#fff',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}
          >
            {visualizations.find(v => v.id === activeView)?.component}
          </section>
        )}
      </main>

      {/* Footer */}
      <footer
        style={{
          maxWidth: '1400px',
          margin: '48px auto 0',
          padding: '24px',
          borderTop: '2px solid #e0e0e0',
          fontSize: '14px',
          color: '#666',
          textAlign: 'center'
        }}
      >
        <p style={{ margin: '0 0 8px 0' }}>
          Built with the <strong>data-viz</strong> skill from ai-design-components
        </p>
        <p style={{ margin: 0 }}>
          Following Anthropic's Skills best practices for progressive disclosure and token efficiency
        </p>
      </footer>
    </div>
  );
}
