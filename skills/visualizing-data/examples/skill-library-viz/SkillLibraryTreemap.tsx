/**
 * Skill Library Treemap Visualization
 *
 * Best for: At-a-glance hierarchical overview
 * Shows: Plugin groups → Individual skills with status color coding
 *
 * Following data-viz skill guidance:
 * - Hierarchical data → Treemap
 * - Colorblind-safe palette (Paul Tol)
 * - WCAG 2.1 AA compliant
 * - Responsive design
 */

import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { skillLibraryData, statusColors, skillLibraryStats } from './skillLibraryData';

// Transform data for Recharts Treemap format
interface TreemapNode {
  name: string;
  size: number;
  fill: string;
  children?: TreemapNode[];
}

const transformDataForTreemap = (): TreemapNode[] => {
  return skillLibraryData.map(group => ({
    name: group.displayName,
    size: group.skills.length,
    fill: statusColors.groupLabel,
    children: group.skills.map(skill => ({
      name: skill.name,
      size: 1, // Each skill has equal weight
      fill: skill.status === 'complete' ? statusColors.complete : statusColors.wip
    }))
  }));
};

// Custom label component with accessibility
const CustomTreemapContent = (props: any) => {
  const { x, y, width, height, name, fill } = props;

  // Only show label if box is large enough
  const showLabel = width > 60 && height > 40;

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={fill}
        stroke={statusColors.groupBorder}
        strokeWidth={2}
        opacity={0.9}
      />
      {showLabel && (
        <text
          x={x + width / 2}
          y={y + height / 2}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="#FFFFFF"
          fontSize={12}
          fontWeight="bold"
          style={{ pointerEvents: 'none' }}
        >
          {name}
        </text>
      )}
    </g>
  );
};

// Custom tooltip with status information
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const isSkill = data.depth === 2; // Skills are at depth 2
    const isComplete = data.fill === statusColors.complete;

    return (
      <div
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: `2px solid ${statusColors.groupBorder}`,
          borderRadius: '4px',
          padding: '8px 12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
        }}
      >
        <p style={{ margin: 0, fontWeight: 'bold', fontSize: '14px' }}>
          {data.name}
        </p>
        {isSkill && (
          <p style={{ margin: '4px 0 0 0', fontSize: '12px', color: data.fill }}>
            Status: {isComplete ? 'Complete ✓' : 'In Progress'}
          </p>
        )}
      </div>
    );
  }
  return null;
};

export function SkillLibraryTreemap() {
  const treemapData = transformDataForTreemap();

  return (
    <div style={{ width: '100%', height: '100%' }}>
      {/* Accessible header */}
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>
          Skill Library Overview (Treemap)
        </h2>
        <p style={{ margin: '8px 0', color: '#666', fontSize: '14px' }}>
          {skillLibraryStats.totalSkills} total skills across {skillLibraryStats.totalPluginGroups} plugin groups
          • {skillLibraryStats.completeSkills} complete • {skillLibraryStats.wipSkills} in progress
        </p>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: '16px', marginBottom: '16px', fontSize: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: 16, height: 16, backgroundColor: statusColors.complete, border: `1px solid ${statusColors.groupBorder}` }} />
          <span>Complete ({skillLibraryStats.completeSkills})</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: 16, height: 16, backgroundColor: statusColors.wip, border: `1px solid ${statusColors.groupBorder}` }} />
          <span>In Progress ({skillLibraryStats.wipSkills})</span>
        </div>
      </div>

      {/* Treemap chart */}
      <figure
        role="img"
        aria-label={`Treemap showing ${skillLibraryStats.totalSkills} skills organized by plugin groups. ${skillLibraryStats.completeSkills} skills are complete, ${skillLibraryStats.wipSkills} are in progress.`}
        style={{ margin: 0 }}
      >
        <ResponsiveContainer width="100%" height={500}>
          <Treemap
            data={treemapData}
            dataKey="size"
            aspectRatio={4 / 3}
            stroke={statusColors.groupBorder}
            content={<CustomTreemapContent />}
          >
            <Tooltip content={<CustomTooltip />} />
          </Treemap>
        </ResponsiveContainer>
      </figure>

      {/* Accessibility: Text alternative */}
      <details style={{ marginTop: '16px', fontSize: '14px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
          View data table alternative
        </summary>
        <table style={{ width: '100%', marginTop: '8px', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5', textAlign: 'left' }}>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Plugin Group</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Skill Name</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {skillLibraryData.map(group =>
              group.skills.map((skill, idx) => (
                <tr key={`${group.name}-${skill.name}`}>
                  {idx === 0 && (
                    <td
                      rowSpan={group.skills.length}
                      style={{ padding: '8px', border: '1px solid #ddd', fontWeight: 'bold' }}
                    >
                      {group.displayName}
                    </td>
                  )}
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>{skill.name}</td>
                  <td
                    style={{
                      padding: '8px',
                      border: '1px solid #ddd',
                      color: skill.status === 'complete' ? statusColors.complete : statusColors.wip,
                      fontWeight: 'bold'
                    }}
                  >
                    {skill.status === 'complete' ? 'Complete ✓' : 'In Progress'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </details>
    </div>
  );
}
