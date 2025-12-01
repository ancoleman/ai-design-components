/**
 * Skill Library Grouped Bar Chart
 *
 * Best for: Comparing plugin groups and showing progress
 * Shows: Complete vs WIP skills per plugin group
 *
 * Following data-viz skill guidance:
 * - Compare categories → Grouped Bar Chart
 * - Colorblind-safe palette (Paul Tol)
 * - WCAG 2.1 AA compliant
 * - Clear labels and legends
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { skillLibraryData, statusColors, skillLibraryStats } from './skillLibraryData';

// Transform data for grouped bar chart
interface BarChartData {
  group: string;
  complete: number;
  wip: number;
  total: number;
  completionRate: number;
}

const transformDataForBarChart = (): BarChartData[] => {
  return skillLibraryData.map(group => {
    const completeCount = group.skills.filter(s => s.status === 'complete').length;
    const wipCount = group.skills.filter(s => s.status === 'wip').length;

    return {
      group: group.displayName,
      complete: completeCount,
      wip: wipCount,
      total: group.skills.length,
      completionRate: group.completionRate
    };
  });
};

// Custom tooltip
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const complete = payload[0].value;
    const wip = payload[1].value;
    const total = complete + wip;
    const percentage = total > 0 ? Math.round((complete / total) * 100) : 0;

    return (
      <div
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: `2px solid ${statusColors.groupBorder}`,
          borderRadius: '4px',
          padding: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
        }}
      >
        <p style={{ margin: 0, fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
          {label}
        </p>
        <div style={{ fontSize: '13px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <div style={{ width: 12, height: 12, backgroundColor: statusColors.complete }} />
            <span>Complete: {complete}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <div style={{ width: 12, height: 12, backgroundColor: statusColors.wip }} />
            <span>In Progress: {wip}</span>
          </div>
          <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #ddd' }}>
            <strong>Total: {total} skills ({percentage}% complete)</strong>
          </div>
        </div>
      </div>
    );
  }
  return null;
};

// Custom legend
const CustomLegend = (props: any) => {
  const { payload } = props;
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', marginTop: '16px' }}>
      {payload.map((entry: any, index: number) => (
        <div key={`legend-${index}`} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div
            style={{
              width: 16,
              height: 16,
              backgroundColor: entry.color,
              border: `1px solid ${statusColors.groupBorder}`
            }}
          />
          <span style={{ fontSize: '14px' }}>{entry.value}</span>
        </div>
      ))}
    </div>
  );
};

export function SkillLibraryBarChart() {
  const barChartData = transformDataForBarChart();

  // Sort by completion rate (descending) for better visual storytelling
  const sortedData = [...barChartData].sort((a, b) => b.completionRate - a.completionRate);

  return (
    <div style={{ width: '100%', height: '100%' }}>
      {/* Accessible header */}
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>
          Skills by Plugin Group (Grouped Bar Chart)
        </h2>
        <p style={{ margin: '8px 0', color: '#666', fontSize: '14px' }}>
          Compare complete vs in-progress skills across {skillLibraryStats.totalPluginGroups} plugin groups
        </p>
      </div>

      {/* Bar chart */}
      <figure
        role="img"
        aria-label={`Bar chart comparing skill completion across plugin groups. Data Skills leads with ${barChartData.find(d => d.group === 'Data Skills')?.completionRate}% completion rate.`}
        style={{ margin: 0 }}
      >
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={sortedData}
            margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis
              dataKey="group"
              angle={-45}
              textAnchor="end"
              height={100}
              interval={0}
              style={{ fontSize: '12px' }}
            />
            <YAxis
              label={{
                value: 'Number of Skills',
                angle: -90,
                position: 'insideLeft',
                style: { fontSize: '14px' }
              }}
              style={{ fontSize: '12px' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend content={<CustomLegend />} />
            <Bar
              dataKey="complete"
              name="Complete"
              fill={statusColors.complete}
              radius={[4, 4, 0, 0]}
            />
            <Bar
              dataKey="wip"
              name="In Progress"
              fill={statusColors.wip}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </figure>

      {/* Summary statistics */}
      <div style={{ marginTop: '24px', padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
        <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', fontWeight: 'bold' }}>
          Summary
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', fontSize: '14px' }}>
          <div>
            <strong>Leading Group:</strong>{' '}
            <span style={{ color: statusColors.complete }}>
              {sortedData[0].group} ({Math.round(sortedData[0].completionRate * 100)}% complete)
            </span>
          </div>
          <div>
            <strong>Overall Progress:</strong>{' '}
            {skillLibraryStats.completeSkills}/{skillLibraryStats.totalSkills} skills complete (
            {Math.round(skillLibraryStats.completionRate * 100)}%)
          </div>
          <div>
            <strong>Groups with Progress:</strong>{' '}
            {sortedData.filter(d => d.complete > 0).length}/{skillLibraryStats.totalPluginGroups}
          </div>
        </div>
      </div>

      {/* Accessibility: Data table alternative */}
      <details style={{ marginTop: '16px', fontSize: '14px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
          View data table alternative
        </summary>
        <table style={{ width: '100%', marginTop: '8px', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5', textAlign: 'left' }}>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Plugin Group</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Complete</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>In Progress</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Total</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Completion %</th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map(row => (
              <tr key={row.group}>
                <td style={{ padding: '8px', border: '1px solid #ddd', fontWeight: 'bold' }}>
                  {row.group}
                </td>
                <td style={{ padding: '8px', border: '1px solid #ddd', color: statusColors.complete }}>
                  {row.complete}
                </td>
                <td style={{ padding: '8px', border: '1px solid #ddd', color: statusColors.wip }}>
                  {row.wip}
                </td>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                  {row.total}
                </td>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                  {Math.round(row.completionRate * 100)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </div>
  );
}
