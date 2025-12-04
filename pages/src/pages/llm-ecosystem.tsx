import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './llm-ecosystem.module.css';

type TabName = 'venn' | 'detailed' | 'architecture' | 'agents' | 'workflows';
type LayerName = 'foundation' | 'protocol' | 'orchestration' | 'application' | 'all';

export default function LLMEcosystem(): JSX.Element {
  const [activeTab, setActiveTab] = useState<TabName>('venn');
  const [activeLayer, setActiveLayer] = useState<LayerName>('foundation');

  return (
    <Layout
      title="LLM Tool Ecosystem"
      description="Professional Services Framework for Understanding Tool Calling, MCP, Agents, LangChain, and Claude-Specific Features"
    >
      <main className={styles.container}>
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>LLM Tool Ecosystem Architecture</h1>
          <p className={styles.tagline}>Professional Services Framework</p>
          <p className={styles.subtitle}>
            Understanding Tool Calling, MCP, Agents, LangChain, and Claude-Specific Features
          </p>
        </div>

        <div className={styles.accentLine} />

        {/* Executive Summary */}
        <div className={styles.insightBox}>
          <h3>Executive Summary</h3>
          <p>
            <strong>These technologies operate at different architectural layers and serve distinct purposes.</strong>{' '}
            They're not competing alternatives—they're complementary systems designed to work together.
          </p>
          <ul>
            <li><strong>Foundation:</strong> Tool Calling enables LLMs to request structured actions</li>
            <li><strong>Protocol:</strong> MCP standardizes integration across systems</li>
            <li><strong>Orchestration:</strong> Agents & Frameworks coordinate complex workflows</li>
            <li><strong>Application:</strong> Skills & Commands provide user-facing capabilities</li>
          </ul>
        </div>

        {/* Tabs */}
        <div className={styles.tabs}>
          {(['venn', 'detailed', 'architecture', 'agents', 'workflows'] as TabName[]).map((tab) => (
            <button
              key={tab}
              className={`${styles.tab} ${activeTab === tab ? styles.tabActive : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab === 'venn' && 'Interactive Venn'}
              {tab === 'detailed' && 'Detailed Comparison'}
              {tab === 'architecture' && 'Architecture Stack'}
              {tab === 'agents' && 'Agents Deep Dive'}
              {tab === 'workflows' && 'Integration Workflows'}
            </button>
          ))}
        </div>

        {/* Venn Tab */}
        <div className={`${styles.tabContent} ${activeTab === 'venn' ? styles.tabContentActive : ''}`}>
          <h2 style={{ textAlign: 'center', marginBottom: '25px' }}>Select Architectural Layer</h2>

          <div className={styles.layerSelector}>
            {[
              { id: 'foundation', color: '#FA582D', label: 'Foundation' },
              { id: 'protocol', color: '#00C0E8', label: 'Protocol' },
              { id: 'orchestration', color: '#C84727', label: 'Orchestration' },
              { id: 'application', color: '#FFCB06', label: 'Application' },
              { id: 'all', color: 'linear-gradient(45deg, #FA582D, #00C0E8, #00CC66, #C84727)', label: 'All Layers' },
            ].map((layer) => (
              <button
                key={layer.id}
                className={`${styles.layerBtn} ${activeLayer === layer.id ? styles.layerBtnActive : ''}`}
                onClick={() => setActiveLayer(layer.id as LayerName)}
              >
                <span
                  className={styles.layerIndicator}
                  style={{ background: layer.color }}
                />
                {layer.label}
              </button>
            ))}
          </div>

          <div className={styles.vennCanvas}>
            {/* Foundation Layer */}
            <div className={`${styles.vennLayer} ${activeLayer === 'foundation' ? styles.vennLayerActive : ''}`}>
              <div
                className={`${styles.vennShape} ${styles.colorToolCalling}`}
                style={{ width: '450px', height: '450px', left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.5em', marginBottom: '12px', fontWeight: 700 }}>Tool/Function Calling</div>
                  <div style={{ fontSize: '0.9em', fontWeight: 600 }}>The Foundation Layer</div>
                </div>
              </div>
              <div className={styles.overlapRegion} style={{ left: '50%', top: '12%', transform: 'translateX(-50%)' }}>
                <div className={styles.overlapTitle}>Core Capability</div>
                <div className={styles.overlapContent}>
                  • LLM generates structured JSON<br />
                  • Specifies function + arguments<br />
                  • ALL systems depend on this<br />
                  • Model suggests, doesn't execute
                </div>
              </div>
            </div>

            {/* Protocol Layer */}
            <div className={`${styles.vennLayer} ${activeLayer === 'protocol' ? styles.vennLayerActive : ''}`}>
              <div
                className={`${styles.vennShape} ${styles.colorMcp}`}
                style={{ width: '400px', height: '400px', left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.5em', marginBottom: '12px', fontWeight: 700 }}>MCP</div>
                  <div style={{ fontSize: '0.9em', fontWeight: 600 }}>Protocol Layer</div>
                </div>
              </div>
              <div className={styles.overlapRegion} style={{ left: '18%', top: '22%' }}>
                <div className={styles.overlapTitle}>Standardization</div>
                <div className={styles.overlapContent}>
                  • Uses tool calling underneath<br />
                  • Client-server architecture<br />
                  • JSON-RPC transport<br />
                  • Dynamic discovery
                </div>
              </div>
              <div className={styles.overlapRegion} style={{ right: '18%', top: '22%' }}>
                <div className={styles.overlapTitle}>Universal Protocol</div>
                <div className={styles.overlapContent}>
                  • "USB-C for AI"<br />
                  • Solves N×M problem<br />
                  • Vendor-agnostic<br />
                  • Growing ecosystem
                </div>
              </div>
            </div>

            {/* Orchestration Layer */}
            <div className={`${styles.vennLayer} ${activeLayer === 'orchestration' ? styles.vennLayerActive : ''}`}>
              <div
                className={`${styles.vennShape} ${styles.colorAgents}`}
                style={{ width: '320px', height: '320px', left: '35%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.4em', marginBottom: '10px', fontWeight: 700 }}>AI Agents</div>
                  <div style={{ fontSize: '0.85em', fontWeight: 600 }}>Autonomous Orchestration</div>
                </div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorLangchain}`}
                style={{ width: '320px', height: '320px', left: '65%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.4em', marginBottom: '10px', fontWeight: 700 }}>LangChain</div>
                  <div style={{ fontSize: '0.85em', fontWeight: 600 }}>Framework Orchestration</div>
                </div>
              </div>
              <div className={styles.overlapRegion} style={{ left: '50%', top: '25%', transform: 'translateX(-50%)' }}>
                <div className={styles.overlapTitle}>Orchestration Layer</div>
                <div className={styles.overlapContent}>
                  <strong>Agents:</strong> LLM-driven decisions<br />
                  <strong>LangChain:</strong> Framework structure<br />
                  Both manage complex workflows
                </div>
              </div>
            </div>

            {/* Application Layer */}
            <div className={`${styles.vennLayer} ${activeLayer === 'application' ? styles.vennLayerActive : ''}`}>
              <div
                className={`${styles.vennShape} ${styles.colorSkills}`}
                style={{ width: '300px', height: '300px', left: '30%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.3em', marginBottom: '10px', fontWeight: 700 }}>Claude Skills</div>
                  <div style={{ fontSize: '0.8em', fontWeight: 600 }}>Model-Invoked</div>
                </div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorCommands}`}
                style={{ width: '300px', height: '300px', left: '70%', top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className={styles.shapeLabel}>
                  <div style={{ fontSize: '1.3em', marginBottom: '10px', fontWeight: 700 }}>/Commands</div>
                  <div style={{ fontSize: '0.8em', fontWeight: 600 }}>User-Invoked</div>
                </div>
              </div>
              <div className={styles.overlapRegion} style={{ left: '50%', top: '28%', transform: 'translateX(-50%)' }}>
                <div className={styles.overlapTitle}>Invocation Difference</div>
                <div className={styles.overlapContent}>
                  <strong>Skills:</strong> Automatic activation<br />
                  <strong>Commands:</strong> Explicit /trigger<br />
                  Both: Markdown-based workflows
                </div>
              </div>
            </div>

            {/* All Layers */}
            <div className={`${styles.vennLayer} ${activeLayer === 'all' ? styles.vennLayerActive : ''}`}>
              <div
                className={`${styles.vennShape} ${styles.colorToolCalling}`}
                style={{ width: '550px', height: '550px', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', opacity: 0.5 }}
              >
                <div className={styles.shapeLabel} style={{ position: 'absolute', top: '8%' }}>Tool Calling</div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorMcp}`}
                style={{ width: '460px', height: '460px', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', opacity: 0.5 }}
              >
                <div className={styles.shapeLabel} style={{ position: 'absolute', top: '15%' }}>MCP</div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorAgents}`}
                style={{ width: '280px', height: '280px', left: '42%', top: '50%', transform: 'translate(-50%, -50%)', opacity: 0.6 }}
              >
                <div className={styles.shapeLabel} style={{ fontSize: '0.95em' }}>Agents</div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorLangchain}`}
                style={{ width: '280px', height: '280px', left: '58%', top: '50%', transform: 'translate(-50%, -50%)', opacity: 0.6 }}
              >
                <div className={styles.shapeLabel} style={{ fontSize: '0.95em' }}>LangChain</div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorSkills}`}
                style={{ width: '160px', height: '160px', left: '38%', top: '58%', transform: 'translate(-50%, -50%)', opacity: 0.7 }}
              >
                <div className={styles.shapeLabel} style={{ fontSize: '0.85em' }}>Skills</div>
              </div>
              <div
                className={`${styles.vennShape} ${styles.colorCommands}`}
                style={{ width: '160px', height: '160px', left: '62%', top: '58%', transform: 'translate(-50%, -50%)', opacity: 0.7 }}
              >
                <div className={styles.shapeLabel} style={{ fontSize: '0.85em' }}>/Commands</div>
              </div>
              <div className={styles.overlapRegion} style={{ left: '50%', bottom: '8%', transform: 'translateX(-50%)' }}>
                <div className={styles.overlapTitle}>Complete Stack</div>
                <div className={styles.overlapContent}>
                  Foundation → Protocol → Orchestration → Application<br />
                  <strong>All layers work together</strong>
                </div>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className={styles.legend}>
            <h4>Color Legend</h4>
            <div className={styles.legendItems}>
              {[
                { color: '#FA582D', label: 'Tool Calling', desc: 'Foundation' },
                { color: '#00C0E8', label: 'MCP', desc: 'Protocol' },
                { color: '#C84727', label: 'Agents', desc: 'Orchestration' },
                { color: '#00CC66', label: 'LangChain', desc: 'Framework' },
                { color: '#FFCB06', label: 'Skills', desc: 'Application' },
                { color: '#FF724D', label: '/Commands', desc: 'Application' },
              ].map((item) => (
                <div key={item.label} className={styles.legendItem}>
                  <div className={styles.legendColor} style={{ background: item.color, borderColor: item.color }} />
                  <span><strong>{item.label}</strong> - {item.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Detailed Comparison Tab */}
        <div className={`${styles.tabContent} ${activeTab === 'detailed' ? styles.tabContentActive : ''}`}>
          <h2 style={{ marginBottom: '30px' }}>Comprehensive Feature Comparison</h2>

          <div className={styles.comparisonTable}>
            <table>
              <thead>
                <tr>
                  <th style={{ width: '200px' }}>Characteristic</th>
                  <th>Tool Calling</th>
                  <th>MCP</th>
                  <th>Agents</th>
                  <th>LangChain</th>
                  <th>Claude Skills</th>
                  <th>/Commands</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Architectural Layer</strong></td>
                  <td>Model capability</td>
                  <td>Protocol/standard</td>
                  <td>Orchestration pattern</td>
                  <td>Framework/library</td>
                  <td>Application feature</td>
                  <td>Application feature</td>
                </tr>
                <tr>
                  <td><strong>Primary Purpose</strong></td>
                  <td>Generate structured function requests</td>
                  <td>Standardize tool integration</td>
                  <td>Autonomous task execution</td>
                  <td>Orchestrate LLM applications</td>
                  <td>Package domain expertise</td>
                  <td>Reusable prompt workflows</td>
                </tr>
                <tr>
                  <td><strong>Autonomy Level</strong></td>
                  <td>None (suggestion only)</td>
                  <td>Low (executes defined tools)</td>
                  <td><strong>High (self-directed)</strong></td>
                  <td>Medium (workflow-directed)</td>
                  <td>Medium (context-triggered)</td>
                  <td>None (user-triggered)</td>
                </tr>
                <tr>
                  <td><strong>Planning Capability</strong></td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />No planning</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />No planning</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Multi-step planning</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconPartial}`} />Chain/workflow planning</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />Predefined instructions</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />Single execution</td>
                </tr>
                <tr>
                  <td><strong>Memory Management</strong></td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />Stateless</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconPartial}`} />Session-based</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Short & long-term memory</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Framework-managed</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconPartial}`} />Per-skill state</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />Stateless</td>
                </tr>
                <tr>
                  <td><strong>Cross-Platform</strong></td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />All LLM providers</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Open standard</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Framework-agnostic</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconYes}`} />Multi-provider</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconPartial}`} />Claude only</td>
                  <td><span className={`${styles.featureIcon} ${styles.iconNo}`} />Claude Code only</td>
                </tr>
                <tr>
                  <td><strong>Best For</strong></td>
                  <td>Simple API calls</td>
                  <td>Multi-system integration</td>
                  <td>Complex autonomous tasks</td>
                  <td>Structured workflows</td>
                  <td>Recurring domain tasks</td>
                  <td>Team workflow shortcuts</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className={styles.insightBox} style={{ marginTop: '40px' }}>
            <h3>Critical Distinction: Workflows vs. Agents</h3>
            <p><strong>Anthropic defines two types of agentic systems:</strong></p>
            <ul style={{ marginTop: '15px', lineHeight: 1.9 }}>
              <li><strong>Workflows:</strong> LLMs and tools orchestrated through predefined code paths</li>
              <li><strong>Agents:</strong> LLMs dynamically direct their own processes and tool usage</li>
            </ul>
            <p style={{ marginTop: '15px' }}>
              <strong>Trade-off:</strong> Workflows offer predictability and consistency. Agents provide flexibility and model-driven decision-making at scale.
            </p>
          </div>
        </div>

        {/* Architecture Tab */}
        <div className={`${styles.tabContent} ${activeTab === 'architecture' ? styles.tabContentActive : ''}`}>
          <h2 style={{ marginBottom: '30px' }}>Architectural Stack & Dependencies</h2>

          <div className={styles.detailPanel} style={{ borderLeftColor: '#FA582D' }}>
            <h3 style={{ color: '#FA582D' }}>Layer 1: Model Capability (Foundation)</h3>
            <div className={styles.detailGrid}>
              <div className={styles.detailCard} style={{ borderLeftColor: '#FA582D' }}>
                <h4>Tool/Function Calling</h4>
                <ul>
                  <li><strong>What:</strong> LLM capability to generate structured function calls</li>
                  <li><strong>How:</strong> Model outputs JSON with function name + arguments</li>
                  <li><strong>Execution:</strong> Model DOES NOT execute - your code must</li>
                  <li><strong>Dependency:</strong> None - this IS the foundation</li>
                  <li><strong>Universal:</strong> OpenAI, Anthropic, Google, Meta, etc.</li>
                </ul>
              </div>
            </div>
          </div>

          <div className={styles.arrow}>⬇</div>

          <div className={styles.detailPanel} style={{ borderLeftColor: '#00C0E8' }}>
            <h3 style={{ color: '#00C0E8' }}>Layer 2: Protocol (Standardization)</h3>
            <div className={styles.detailGrid}>
              <div className={styles.detailCard} style={{ borderLeftColor: '#00C0E8' }}>
                <h4>Model Context Protocol (MCP)</h4>
                <ul>
                  <li><strong>What:</strong> Open standard for tool integration</li>
                  <li><strong>Architecture:</strong> Client-server with JSON-RPC</li>
                  <li><strong>Components:</strong> MCP Client, Server, Host</li>
                  <li><strong>Builds on:</strong> Tool calling (uses internally)</li>
                  <li><strong>Value:</strong> Solves N×M problem, dynamic discovery</li>
                </ul>
              </div>
            </div>
          </div>

          <div className={styles.arrow}>⬇</div>

          <div className={styles.detailPanel} style={{ borderLeftColor: '#C84727' }}>
            <h3 style={{ color: '#C84727' }}>Layer 3: Orchestration (Coordination)</h3>
            <div className={styles.detailGrid}>
              <div className={styles.detailCard} style={{ borderLeftColor: '#C84727' }}>
                <h4>AI Agents (Autonomous)</h4>
                <ul>
                  <li><strong>What:</strong> LLM-driven autonomous systems</li>
                  <li><strong>Components:</strong> Agent core, Memory, Planning, Tools</li>
                  <li><strong>Decision-making:</strong> Model directs its own process</li>
                  <li><strong>Builds on:</strong> Tool calling + optionally MCP</li>
                </ul>
              </div>
              <div className={styles.detailCard} style={{ borderLeftColor: '#00CC66' }}>
                <h4>LangChain (Structured)</h4>
                <ul>
                  <li><strong>What:</strong> Framework for LLM applications</li>
                  <li><strong>Components:</strong> Tools, Agents, Chains, Memory</li>
                  <li><strong>Decision-making:</strong> Predefined workflows</li>
                  <li><strong>Builds on:</strong> Tool calling + MCP adapters</li>
                </ul>
              </div>
            </div>
          </div>

          <div className={styles.arrow}>⬇</div>

          <div className={styles.detailPanel} style={{ borderLeftColor: '#FFCB06' }}>
            <h3 style={{ color: '#B38904' }}>Layer 4: Application (User Experience)</h3>
            <div className={styles.detailGrid}>
              <div className={styles.detailCard} style={{ borderLeftColor: '#FFCB06' }}>
                <h4>Claude Skills (Model-Invoked)</h4>
                <ul>
                  <li><strong>What:</strong> Filesystem-based capability packages</li>
                  <li><strong>Structure:</strong> SKILL.md + scripts/resources</li>
                  <li><strong>Invocation:</strong> Automatic (context-triggered)</li>
                  <li><strong>Value:</strong> Progressive disclosure, automation</li>
                </ul>
              </div>
              <div className={styles.detailCard} style={{ borderLeftColor: '#FF724D' }}>
                <h4>Claude /Commands (User-Invoked)</h4>
                <ul>
                  <li><strong>What:</strong> Reusable prompt workflows</li>
                  <li><strong>Structure:</strong> Markdown with frontmatter</li>
                  <li><strong>Invocation:</strong> Explicit /command trigger</li>
                  <li><strong>Value:</strong> Team sharing, explicit control</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Agents Tab */}
        <div className={`${styles.tabContent} ${activeTab === 'agents' ? styles.tabContentActive : ''}`}>
          <h2 style={{ marginBottom: '30px' }}>AI Agents: Deep Dive</h2>

          <div className={styles.insightBox}>
            <h3>What Are AI Agents?</h3>
            <p>
              <strong>AI Agents are systems where LLMs dynamically direct their own processes and tool usage,</strong>{' '}
              maintaining control over how they accomplish tasks. Unlike workflows with predefined paths, agents make autonomous decisions based on their "understanding" of the goal.
            </p>
          </div>

          <div className={styles.detailPanel} style={{ borderLeftColor: '#C84727' }}>
            <h3 style={{ color: '#C84727' }}>Core Agent Components</h3>
            <div className={styles.detailGrid}>
              <div className={styles.detailCard} style={{ borderLeftColor: '#C84727' }}>
                <h4>1. Agent Core (Brain)</h4>
                <ul>
                  <li>LLM serves as the reasoning engine</li>
                  <li>Interprets goals and makes decisions</li>
                  <li>Coordinates all other components</li>
                </ul>
              </div>
              <div className={styles.detailCard} style={{ borderLeftColor: '#FA582D' }}>
                <h4>2. Planning Module</h4>
                <ul>
                  <li>Breaks down complex tasks into steps</li>
                  <li>Creates execution strategies</li>
                  <li>Adapts plans based on feedback</li>
                </ul>
              </div>
              <div className={styles.detailCard} style={{ borderLeftColor: '#00C0E8' }}>
                <h4>3. Memory System</h4>
                <ul>
                  <li><strong>Short-term:</strong> Current task context</li>
                  <li><strong>Long-term:</strong> Historical knowledge</li>
                  <li>Experience accumulation</li>
                </ul>
              </div>
              <div className={styles.detailCard} style={{ borderLeftColor: '#00CC66' }}>
                <h4>4. Tool Integration</h4>
                <ul>
                  <li>Dynamic tool selection</li>
                  <li>Uses tool calling underneath</li>
                  <li>Can integrate MCP servers</li>
                </ul>
              </div>
            </div>
          </div>

          <div className={styles.workflowExample} style={{ borderLeftColor: '#C84727', marginTop: '30px' }}>
            <h4 style={{ color: '#C84727' }}>Agent Execution Flow</h4>
            <div className={styles.workflowSteps}>
              {[
                { num: 1, title: 'Goal Interpretation', desc: 'Agent receives high-level goal: "Analyze Q3 sales data and create executive report"' },
                { num: 2, title: 'Planning', desc: 'Agent creates plan: (1) Retrieve data, (2) Analyze trends, (3) Generate visualizations, (4) Write report' },
                { num: 3, title: 'Tool Selection', desc: 'Agent decides: Use database MCP server → Python for analysis → Visualization library → Document creation' },
                { num: 4, title: 'Execution & Adaptation', desc: 'Agent executes plan, monitors results, adapts if tools fail or data is unexpected' },
                { num: 5, title: 'Memory Update', desc: 'Agent stores learnings: Q3 patterns, successful tool combinations, report preferences' },
              ].map((step) => (
                <div key={step.num} className={styles.workflowStep} style={{ borderLeftColor: '#C84727' }}>
                  <div className={styles.stepNumber}>{step.num}</div>
                  <div className={styles.stepContent}>
                    <strong>{step.title}</strong>
                    {step.desc}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.insightBox} style={{ marginTop: '30px' }}>
            <h3>Agent Challenges & Considerations</h3>
            <p><strong>Agents trade predictability for flexibility:</strong></p>
            <ul style={{ marginTop: '15px' }}>
              <li><strong>Non-deterministic:</strong> Same input may produce different execution paths</li>
              <li><strong>Hallucination risk:</strong> Agent may "invent" data or tool capabilities</li>
              <li><strong>Higher latency:</strong> Multiple LLM calls for planning and execution</li>
              <li><strong>Higher cost:</strong> More tokens consumed for reasoning and iteration</li>
            </ul>
            <p style={{ marginTop: '15px' }}>
              <strong>Recommendation:</strong> Use workflows for well-defined tasks. Use agents when flexibility justifies the complexity.
            </p>
          </div>
        </div>

        {/* Workflows Tab */}
        <div className={`${styles.tabContent} ${activeTab === 'workflows' ? styles.tabContentActive : ''}`}>
          <h2 style={{ marginBottom: '30px' }}>Real-World Integration Workflows</h2>

          <div className={styles.workflowExample} style={{ borderLeftColor: '#FA582D' }}>
            <h4 style={{ color: '#FA582D' }}>Scenario 1: Professional Services RAG System</h4>
            <p><strong>Goal:</strong> Query 50+ GitLab repositories with contextual understanding</p>
            <div className={styles.workflowSteps}>
              {[
                { num: 1, title: 'Foundation: Tool Calling', desc: 'Claude uses tool calling to decide: retrieve from vector DB or generate from knowledge', color: '#FA582D' },
                { num: 2, title: 'Protocol: MCP Servers', desc: 'GitLab MCP (code access), Qdrant MCP (vector search), Vertex AI MCP (embeddings)', color: '#00C0E8' },
                { num: 3, title: 'Orchestration: Agent (Optional)', desc: 'For complex queries, agent decides: which repos to search, what patterns to identify', color: '#C84727' },
                { num: 4, title: 'Application: Claude Skills', desc: 'Security analysis skill auto-activates, applies best practices, generates formatted documentation', color: '#FFCB06' },
              ].map((step) => (
                <div key={step.num} className={styles.workflowStep} style={{ borderLeftColor: step.color }}>
                  <div className={styles.stepNumber}>{step.num}</div>
                  <div className={styles.stepContent}>
                    <strong>{step.title}</strong>
                    {step.desc}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.workflowExample} style={{ borderLeftColor: '#00CC66' }}>
            <h4 style={{ color: '#00CC66' }}>Scenario 2: Claude Code Development Workflow</h4>
            <p><strong>Goal:</strong> Streamline development with automated review, testing, and deployment</p>
            <div className={styles.workflowSteps}>
              {[
                { num: 1, title: '/Commands for Workflows', desc: '/review, /test, /security-scan, /deploy - Team-shared explicit triggers', color: '#FF724D' },
                { num: 2, title: 'Skills for Automation', desc: 'Security analysis skill auto-runs on commits, test generation skill activates on new features', color: '#FFCB06' },
                { num: 3, title: 'MCP for Integration', desc: 'GitHub MCP (PRs), Linear MCP (tasks), Sentry MCP (errors), Jenkins MCP (CI/CD)', color: '#00C0E8' },
                { num: 4, title: 'Tool Calling', desc: 'Enables Claude to invoke all commands, skills, and MCP tools', color: '#FA582D' },
              ].map((step) => (
                <div key={step.num} className={styles.workflowStep} style={{ borderLeftColor: step.color }}>
                  <div className={styles.stepNumber}>{step.num}</div>
                  <div className={styles.stepContent}>
                    <strong>{step.title}</strong>
                    {step.desc}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.insightBox} style={{ marginTop: '40px' }}>
            <h3>Integration Best Practices</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '25px', marginTop: '20px' }}>
              <div>
                <strong>Start Simple</strong><br />
                Begin with tool calling. Add MCP when you need multiple integrations. Add agents when orchestration becomes complex.
              </div>
              <div>
                <strong>Right Abstraction</strong><br />
                Don't use agents for deterministic workflows. Don't reinvent what MCP solves. Choose the appropriate layer.
              </div>
              <div>
                <strong>Consider Lock-in</strong><br />
                Open standards (MCP, tool calling) vs. proprietary (Claude features) vs. framework-dependent (LangChain)
              </div>
              <div>
                <strong>Progressive Enhancement</strong><br />
                Foundation → Protocol → Orchestration → Application. Build from bottom up.
              </div>
            </div>
          </div>
        </div>

        {/* Takeaways */}
        <div className={styles.takeaways}>
          <h2>Key Takeaways</h2>
          <div className={styles.takeawaysGrid}>
            <div className={styles.takeawayCard}>
              <div className="emoji">🏗️</div>
              <strong>Different Layers</strong>
              <span>Foundation → Protocol → Orchestration → Application. Each layer builds on the layers below.</span>
            </div>
            <div className={styles.takeawayCard}>
              <div className="emoji">🤖</div>
              <strong>Agents Are Different</strong>
              <span>Agents provide autonomy at the cost of predictability. Use for complex, adaptive tasks.</span>
            </div>
            <div className={styles.takeawayCard}>
              <div className="emoji">🔗</div>
              <strong>They Work Together</strong>
              <span>Combine layers strategically. Agents + MCP + Skills is powerful for Professional Services.</span>
            </div>
            <div className={styles.takeawayCard}>
              <div className="emoji">⚖️</div>
              <strong>Trade-offs Matter</strong>
              <span>Autonomy vs. control, flexibility vs. predictability, simplicity vs. power.</span>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
