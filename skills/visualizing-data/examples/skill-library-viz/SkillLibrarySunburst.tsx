/**
 * Skill Library Sunburst Chart
 *
 * Best for: Interactive hierarchical exploration
 * Shows: Radial hierarchy with plugin groups (inner ring) and skills (outer ring)
 *
 * Following data-viz skill guidance:
 * - Hierarchical data → Sunburst
 * - Custom visualization → D3.js
 * - Colorblind-safe palette
 * - Interactive drill-down
 * - WCAG 2.1 AA compliant
 */

import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import { skillLibraryData, statusColors, skillLibraryStats } from './skillLibraryData';

// Transform data for D3 hierarchy
interface SunburstNode {
  name: string;
  children?: SunburstNode[];
  value?: number;
  status?: string;
  group?: string;
}

const transformDataForSunburst = (): SunburstNode => {
  return {
    name: 'Skill Library',
    children: skillLibraryData.map(group => ({
      name: group.displayName,
      group: group.name,
      children: group.skills.map(skill => ({
        name: skill.name,
        value: 1,
        status: skill.status,
        group: group.name
      }))
    }))
  };
};

export function SkillLibrarySunburst() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [hoveredNode, setHoveredNode] = useState<{ name: string; type: string; status?: string } | null>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear previous render
    d3.select(svgRef.current).selectAll('*').remove();

    const width = 600;
    const height = 600;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .style('font-family', 'sans-serif')
      .style('font-size', '12px');

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    // Create hierarchy
    const hierarchyData = transformDataForSunburst();
    const root = d3.hierarchy(hierarchyData)
      .sum((d: any) => d.value || 0)
      .sort((a, b) => (b.value || 0) - (a.value || 0));

    // Create partition layout
    const partition = d3.partition<SunburstNode>()
      .size([2 * Math.PI, radius]);

    partition(root);

    // Arc generator
    const arc = d3.arc<d3.HierarchyRectangularNode<SunburstNode>>()
      .startAngle(d => d.x0)
      .endAngle(d => d.x1)
      .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
      .padRadius(radius / 2)
      .innerRadius(d => d.y0)
      .outerRadius(d => d.y1 - 1);

    // Color function
    const getColor = (d: d3.HierarchyRectangularNode<SunburstNode>) => {
      if (d.depth === 0) return '#FFFFFF'; // Center (root)
      if (d.depth === 1) return statusColors.groupLabel; // Plugin groups
      // Individual skills
      return d.data.status === 'complete' ? statusColors.complete : statusColors.wip;
    };

    // Create arcs
    const paths = g.selectAll('path')
      .data(root.descendants().filter(d => d.depth > 0)) // Skip root
      .join('path')
      .attr('d', arc as any)
      .attr('fill', getColor)
      .attr('stroke', '#FFFFFF')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .style('opacity', 0.9)
      .on('mouseenter', function(event, d) {
        d3.select(this).style('opacity', 1);
        setHoveredNode({
          name: d.data.name,
          type: d.depth === 1 ? 'Plugin Group' : 'Skill',
          status: d.data.status
        });
      })
      .on('mouseleave', function() {
        d3.select(this).style('opacity', 0.9);
        setHoveredNode(null);
      })
      .on('click', function(event, d) {
        setSelectedNode(d.data.name);
      });

    // Add labels for plugin groups (inner ring)
    g.selectAll('text')
      .data(root.descendants().filter(d => d.depth === 1))
      .join('text')
      .attr('transform', d => {
        const angle = ((d.x0 + d.x1) / 2) * 180 / Math.PI;
        const rotate = angle - 90;
        const radius = (d.y0 + d.y1) / 2;
        return `rotate(${rotate}) translate(${radius},0) rotate(${angle > 180 ? 180 : 0})`;
      })
      .attr('text-anchor', 'middle')
      .attr('fill', '#FFFFFF')
      .attr('font-weight', 'bold')
      .attr('font-size', '11px')
      .style('pointer-events', 'none')
      .text(d => {
        const arcLength = (d.x1 - d.x0) * (d.y0 + d.y1) / 2;
        return arcLength > 50 ? d.data.name : '';
      });

    // Add center label
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '-0.5em')
      .attr('font-size', '18px')
      .attr('font-weight', 'bold')
      .text('Skill Library');

    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '1em')
      .attr('font-size', '14px')
      .attr('fill', '#666')
      .text(`${skillLibraryStats.totalSkills} skills`);

  }, []);

  return (
    <div style={{ width: '100%', height: '100%' }}>
      {/* Accessible header */}
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>
          Skill Library Hierarchy (Sunburst Chart)
        </h2>
        <p style={{ margin: '8px 0', color: '#666', fontSize: '14px' }}>
          Interactive radial visualization: Inner ring = plugin groups, Outer ring = individual skills
        </p>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: '16px', marginBottom: '16px', fontSize: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: 16, height: 16, backgroundColor: statusColors.groupLabel, border: `1px solid ${statusColors.groupBorder}` }} />
          <span>Plugin Group</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: 16, height: 16, backgroundColor: statusColors.complete, border: `1px solid ${statusColors.groupBorder}` }} />
          <span>Complete ({skillLibraryStats.completeSkills})</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: 16, height: 16, backgroundColor: statusColors.wip, border: `1px solid ${statusColors.groupBorder}` }} />
          <span>In Progress ({skillLibraryStats.wipSkills})</span>
        </div>
      </div>

      {/* Sunburst chart */}
      <figure
        role="img"
        aria-label={`Sunburst chart showing hierarchical structure of ${skillLibraryStats.totalSkills} skills across ${skillLibraryStats.totalPluginGroups} plugin groups. ${skillLibraryStats.completeSkills} skills are complete.`}
        style={{ margin: 0, display: 'flex', justifyContent: 'center' }}
      >
        <svg ref={svgRef} style={{ maxWidth: '100%', height: 'auto' }} />
      </figure>

      {/* Tooltip/Status display */}
      {hoveredNode && (
        <div
          style={{
            marginTop: '16px',
            padding: '12px',
            backgroundColor: '#f5f5f5',
            borderRadius: '4px',
            fontSize: '14px'
          }}
          role="status"
          aria-live="polite"
        >
          <strong>{hoveredNode.type}:</strong> {hoveredNode.name}
          {hoveredNode.status && (
            <span style={{ marginLeft: '12px', color: hoveredNode.status === 'complete' ? statusColors.complete : statusColors.wip }}>
              ({hoveredNode.status === 'complete' ? 'Complete ✓' : 'In Progress'})
            </span>
          )}
        </div>
      )}

      {/* Selected node info */}
      {selectedNode && (
        <div
          style={{
            marginTop: '16px',
            padding: '12px',
            backgroundColor: '#e3f2fd',
            border: '2px solid #2196f3',
            borderRadius: '4px',
            fontSize: '14px'
          }}
        >
          <strong>Selected:</strong> {selectedNode}
          <button
            onClick={() => setSelectedNode(null)}
            style={{
              marginLeft: '12px',
              padding: '4px 8px',
              border: 'none',
              backgroundColor: '#2196f3',
              color: 'white',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '12px'
            }}
          >
            Clear
          </button>
        </div>
      )}

      {/* Interaction instructions */}
      <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#fffde7', borderRadius: '4px', fontSize: '13px' }}>
        <strong>💡 Tip:</strong> Hover over segments to see details. Click to select a skill or plugin group.
      </div>

      {/* Accessibility: Data table alternative */}
      <details style={{ marginTop: '16px', fontSize: '14px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
          View data table alternative
        </summary>
        <table style={{ width: '100%', marginTop: '8px', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5', textAlign: 'left' }}>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Level</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Name</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Status</th>
              <th style={{ padding: '8px', border: '1px solid #ddd' }}>Parent</th>
            </tr>
          </thead>
          <tbody>
            {skillLibraryData.map(group =>
              [
                <tr key={group.name}>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>Plugin Group</td>
                  <td style={{ padding: '8px', border: '1px solid #ddd', fontWeight: 'bold' }}>
                    {group.displayName}
                  </td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                    {group.skills.filter(s => s.status === 'complete').length}/{group.skills.length} complete
                  </td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>Root</td>
                </tr>,
                ...group.skills.map(skill => (
                  <tr key={`${group.name}-${skill.name}`}>
                    <td style={{ padding: '8px', border: '1px solid #ddd', paddingLeft: '24px' }}>Skill</td>
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
                    <td style={{ padding: '8px', border: '1px solid #ddd' }}>{group.displayName}</td>
                  </tr>
                ))
              ]
            )}
          </tbody>
        </table>
      </details>
    </div>
  );
}
