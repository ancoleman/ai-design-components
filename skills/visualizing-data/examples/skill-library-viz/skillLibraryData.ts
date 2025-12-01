/**
 * Skill Library Data Structure
 * Real data from ai-design-components marketplace.json
 */

export type SkillStatus = 'complete' | 'wip';

export interface Skill {
  name: string;
  path: string;
  status: SkillStatus;
}

export interface PluginGroup {
  name: string;
  displayName: string;
  description: string;
  skills: Skill[];
  completionRate: number; // 0-1
}

export const skillLibraryData: PluginGroup[] = [
  {
    name: 'ui-foundation-skills',
    displayName: 'Foundation',
    description: 'Design system including tokens and theming',
    completionRate: 0,
    skills: [
      { name: 'design-tokens', path: './skills/design-tokens', status: 'wip' }
    ]
  },
  {
    name: 'ui-data-skills',
    displayName: 'Data Skills',
    description: 'Data visualization, tables, and dashboards',
    completionRate: 0.67, // 2 of 3 complete
    skills: [
      { name: 'data-viz', path: './skills/data-viz', status: 'complete' },
      { name: 'tables', path: './skills/tables', status: 'wip' },
      { name: 'dashboards', path: './skills/dashboards', status: 'wip' }
    ]
  },
  {
    name: 'ui-input-skills',
    displayName: 'Input Skills',
    description: 'Form systems, search, and filter components',
    completionRate: 0.5, // 1 of 2 complete
    skills: [
      { name: 'forms', path: './skills/forms', status: 'complete' },
      { name: 'search-filter', path: './skills/search-filter', status: 'wip' }
    ]
  },
  {
    name: 'ui-interaction-skills',
    displayName: 'Interaction Skills',
    description: 'AI chat, drag-drop, and feedback systems',
    completionRate: 0,
    skills: [
      { name: 'ai-chat', path: './skills/ai-chat', status: 'wip' },
      { name: 'drag-drop', path: './skills/drag-drop', status: 'wip' },
      { name: 'feedback', path: './skills/feedback', status: 'wip' }
    ]
  },
  {
    name: 'ui-structure-skills',
    displayName: 'Structure Skills',
    description: 'Navigation, layout, and timeline components',
    completionRate: 0,
    skills: [
      { name: 'navigation', path: './skills/navigation', status: 'wip' },
      { name: 'layout', path: './skills/layout', status: 'wip' },
      { name: 'timeline', path: './skills/timeline', status: 'wip' }
    ]
  },
  {
    name: 'ui-content-skills',
    displayName: 'Content Skills',
    description: 'Media management and user onboarding',
    completionRate: 0,
    skills: [
      { name: 'media', path: './skills/media', status: 'wip' },
      { name: 'onboarding', path: './skills/onboarding', status: 'wip' }
    ]
  }
];

// Summary statistics
export const skillLibraryStats = {
  totalSkills: 14,
  completeSkills: 2,
  wipSkills: 12,
  totalPluginGroups: 6,
  completionRate: 2 / 14, // ~14.3%
  completePluginGroups: ['ui-data-skills', 'ui-input-skills'] // Partially complete
};

// Color scheme (colorblind-safe from Paul Tol palette)
export const statusColors = {
  complete: '#228833', // Green
  wip: '#FFB000', // Yellow/Orange
  groupLabel: '#4477AA', // Blue
  groupBorder: '#CCCCCC'
};

// Flatten for certain visualization types
export const flatSkillData = skillLibraryData.flatMap(group =>
  group.skills.map(skill => ({
    ...skill,
    group: group.name,
    groupDisplayName: group.displayName
  }))
);
