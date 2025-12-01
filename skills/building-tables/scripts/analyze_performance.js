#!/usr/bin/env node

/**
 * Table Performance Analyzer
 * Benchmarks table rendering performance and identifies bottlenecks
 */

class TablePerformanceAnalyzer {
  constructor() {
    this.metrics = {
      renderTime: [],
      scrollFPS: [],
      memoryUsage: [],
      reRenderTime: [],
      sortTime: [],
      filterTime: []
    };
  }

  /**
   * Measure initial render performance
   */
  measureRenderTime(rowCount, columnCount) {
    const startTime = performance.now();

    // Simulate table render
    const table = this.createVirtualTable(rowCount, columnCount);

    const endTime = performance.now();
    const renderTime = endTime - startTime;

    this.metrics.renderTime.push({
      rows: rowCount,
      columns: columnCount,
      time: renderTime,
      throughput: (rowCount * columnCount) / renderTime * 1000 // cells per second
    });

    return renderTime;
  }

  /**
   * Create virtual table structure for testing
   */
  createVirtualTable(rows, columns) {
    const table = [];
    for (let i = 0; i < rows; i++) {
      const row = [];
      for (let j = 0; j < columns; j++) {
        row.push({
          value: `Cell ${i}-${j}`,
          metadata: {
            row: i,
            column: j,
            isSelected: false,
            isEditable: true
          }
        });
      }
      table.push(row);
    }
    return table;
  }

  /**
   * Measure scroll performance
   */
  measureScrollPerformance(rowCount, visibleRows = 20) {
    const frames = [];
    const duration = 1000; // 1 second of scrolling
    const targetFPS = 60;
    const frameTime = 1000 / targetFPS;

    let currentPosition = 0;
    let frameCount = 0;
    const maxPosition = rowCount - visibleRows;

    const startTime = performance.now();

    // Simulate scrolling
    while (performance.now() - startTime < duration) {
      const frameStart = performance.now();

      // Simulate viewport update
      currentPosition = Math.min(currentPosition + 10, maxPosition);
      this.renderViewport(currentPosition, visibleRows);

      const frameEnd = performance.now();
      const frameDuration = frameEnd - frameStart;

      frames.push(frameDuration);
      frameCount++;

      // If we've scrolled to the end, reset
      if (currentPosition >= maxPosition) {
        currentPosition = 0;
      }
    }

    const averageFPS = frameCount / (duration / 1000);
    const droppedFrames = frames.filter(f => f > frameTime).length;

    this.metrics.scrollFPS.push({
      rows: rowCount,
      averageFPS: Math.round(averageFPS),
      droppedFrames,
      smoothness: ((frameCount - droppedFrames) / frameCount * 100).toFixed(2)
    });

    return averageFPS;
  }

  /**
   * Simulate viewport rendering
   */
  renderViewport(startRow, visibleRows) {
    const viewport = [];
    for (let i = startRow; i < startRow + visibleRows; i++) {
      viewport.push({ row: i, rendered: true });
    }
    return viewport;
  }

  /**
   * Measure sorting performance
   */
  measureSortPerformance(data, columnIndex = 0) {
    const startTime = performance.now();

    // Clone data to avoid mutation
    const sortedData = [...data].sort((a, b) => {
      const aVal = a[columnIndex]?.value || '';
      const bVal = b[columnIndex]?.value || '';
      return aVal.localeCompare(bVal);
    });

    const endTime = performance.now();
    const sortTime = endTime - startTime;

    this.metrics.sortTime.push({
      rows: data.length,
      time: sortTime,
      itemsPerSecond: (data.length / sortTime * 1000).toFixed(0)
    });

    return sortTime;
  }

  /**
   * Measure filtering performance
   */
  measureFilterPerformance(data, filterTerm = 'Cell') {
    const startTime = performance.now();

    const filteredData = data.filter(row =>
      row.some(cell =>
        cell.value.toLowerCase().includes(filterTerm.toLowerCase())
      )
    );

    const endTime = performance.now();
    const filterTime = endTime - startTime;

    this.metrics.filterTime.push({
      rows: data.length,
      filtered: filteredData.length,
      time: filterTime,
      throughput: (data.length / filterTime * 1000).toFixed(0)
    });

    return filterTime;
  }

  /**
   * Measure memory usage
   */
  measureMemoryUsage(rowCount) {
    if (typeof process !== 'undefined' && process.memoryUsage) {
      const usage = process.memoryUsage();
      this.metrics.memoryUsage.push({
        rows: rowCount,
        heapUsed: (usage.heapUsed / 1024 / 1024).toFixed(2), // MB
        heapTotal: (usage.heapTotal / 1024 / 1024).toFixed(2), // MB
        rss: (usage.rss / 1024 / 1024).toFixed(2) // MB
      });
      return usage.heapUsed;
    }
    return null;
  }

  /**
   * Simulate virtual scrolling performance
   */
  measureVirtualScrolling(totalRows, viewportRows = 20) {
    const windowSize = viewportRows * 3; // Typical buffer
    const metrics = {
      totalRows,
      viewportRows,
      windowSize,
      memoryEstimate: (windowSize * 100) / 1024 + ' KB', // ~100 bytes per row
      domNodes: windowSize,
      constantComplexity: true
    };

    return metrics;
  }

  /**
   * Generate performance report
   */
  generateReport() {
    console.log('\n═══════════════════════════════════════');
    console.log('    TABLE PERFORMANCE ANALYSIS REPORT   ');
    console.log('═══════════════════════════════════════\n');

    // Render Performance
    if (this.metrics.renderTime.length > 0) {
      console.log('📊 RENDER PERFORMANCE');
      console.log('────────────────────');
      this.metrics.renderTime.forEach(metric => {
        const grade = this.gradeRenderTime(metric.time, metric.rows);
        console.log(`  ${metric.rows} rows × ${metric.columns} columns:`);
        console.log(`  ⏱  Time: ${metric.time.toFixed(2)}ms ${grade}`);
        console.log(`  📈 Throughput: ${metric.throughput.toFixed(0)} cells/sec`);
        console.log('');
      });
    }

    // Scroll Performance
    if (this.metrics.scrollFPS.length > 0) {
      console.log('📜 SCROLL PERFORMANCE');
      console.log('────────────────────');
      this.metrics.scrollFPS.forEach(metric => {
        const grade = this.gradeFPS(metric.averageFPS);
        console.log(`  ${metric.rows} rows:`);
        console.log(`  🎯 FPS: ${metric.averageFPS} ${grade}`);
        console.log(`  📉 Dropped frames: ${metric.droppedFrames}`);
        console.log(`  ✨ Smoothness: ${metric.smoothness}%`);
        console.log('');
      });
    }

    // Sort Performance
    if (this.metrics.sortTime.length > 0) {
      console.log('🔄 SORT PERFORMANCE');
      console.log('────────────────────');
      this.metrics.sortTime.forEach(metric => {
        const grade = this.gradeSortTime(metric.time, metric.rows);
        console.log(`  ${metric.rows} rows:`);
        console.log(`  ⏱  Time: ${metric.time.toFixed(2)}ms ${grade}`);
        console.log(`  📊 Items/sec: ${metric.itemsPerSecond}`);
        console.log('');
      });
    }

    // Filter Performance
    if (this.metrics.filterTime.length > 0) {
      console.log('🔍 FILTER PERFORMANCE');
      console.log('─────────────────────');
      this.metrics.filterTime.forEach(metric => {
        const grade = this.gradeFilterTime(metric.time, metric.rows);
        console.log(`  ${metric.rows} rows → ${metric.filtered} results:`);
        console.log(`  ⏱  Time: ${metric.time.toFixed(2)}ms ${grade}`);
        console.log(`  📊 Throughput: ${metric.throughput} rows/sec`);
        console.log('');
      });
    }

    // Memory Usage
    if (this.metrics.memoryUsage.length > 0) {
      console.log('💾 MEMORY USAGE');
      console.log('───────────────');
      this.metrics.memoryUsage.forEach(metric => {
        console.log(`  ${metric.rows} rows:`);
        console.log(`  📦 Heap Used: ${metric.heapUsed} MB`);
        console.log(`  📊 Total Heap: ${metric.heapTotal} MB`);
        console.log(`  🖥  RSS: ${metric.rss} MB`);
        console.log('');
      });
    }

    // Recommendations
    this.printRecommendations();
  }

  /**
   * Grade performance metrics
   */
  gradeRenderTime(time, rows) {
    const msPerRow = time / rows;
    if (msPerRow < 0.1) return '✅ Excellent';
    if (msPerRow < 0.5) return '🟢 Good';
    if (msPerRow < 1) return '🟡 Fair';
    return '🔴 Poor';
  }

  gradeFPS(fps) {
    if (fps >= 60) return '✅ Perfect';
    if (fps >= 50) return '🟢 Good';
    if (fps >= 30) return '🟡 Fair';
    return '🔴 Poor';
  }

  gradeSortTime(time, rows) {
    const msPerRow = time / rows;
    if (msPerRow < 0.01) return '✅ Excellent';
    if (msPerRow < 0.05) return '🟢 Good';
    if (msPerRow < 0.1) return '🟡 Fair';
    return '🔴 Poor';
  }

  gradeFilterTime(time, rows) {
    const msPerRow = time / rows;
    if (msPerRow < 0.01) return '✅ Excellent';
    if (msPerRow < 0.05) return '🟢 Good';
    if (msPerRow < 0.1) return '🟡 Fair';
    return '🔴 Poor';
  }

  /**
   * Print performance recommendations
   */
  printRecommendations() {
    console.log('\n💡 RECOMMENDATIONS');
    console.log('═════════════════════════════════════');

    const recommendations = [];

    // Check render performance
    const lastRender = this.metrics.renderTime[this.metrics.renderTime.length - 1];
    if (lastRender && lastRender.rows > 1000 && lastRender.time > 500) {
      recommendations.push({
        issue: 'Slow initial render for large dataset',
        solution: 'Consider implementing virtual scrolling or pagination'
      });
    }

    // Check scroll performance
    const lastScroll = this.metrics.scrollFPS[this.metrics.scrollFPS.length - 1];
    if (lastScroll && lastScroll.averageFPS < 50) {
      recommendations.push({
        issue: 'Poor scroll performance',
        solution: 'Implement virtual scrolling to maintain 60fps'
      });
    }

    // Check memory usage
    const lastMemory = this.metrics.memoryUsage[this.metrics.memoryUsage.length - 1];
    if (lastMemory && parseFloat(lastMemory.heapUsed) > 100) {
      recommendations.push({
        issue: 'High memory usage',
        solution: 'Use virtual scrolling to reduce DOM nodes'
      });
    }

    if (recommendations.length === 0) {
      console.log('  ✅ Performance looks good!');
      console.log('  Continue monitoring as data grows.');
    } else {
      recommendations.forEach((rec, index) => {
        console.log(`\n  ${index + 1}. ⚠️  ${rec.issue}`);
        console.log(`     💡 ${rec.solution}`);
      });
    }

    console.log('\n═════════════════════════════════════\n');
  }

  /**
   * Run complete benchmark suite
   */
  runBenchmark(options = {}) {
    const {
      rowCounts = [100, 1000, 10000],
      columnCount = 10
    } = options;

    console.log('Starting performance benchmark...\n');

    rowCounts.forEach(rowCount => {
      console.log(`Testing with ${rowCount} rows...`);

      // Create test data
      const data = this.createVirtualTable(rowCount, columnCount);

      // Run tests
      this.measureRenderTime(rowCount, columnCount);
      this.measureScrollPerformance(rowCount);
      this.measureSortPerformance(data);
      this.measureFilterPerformance(data);
      this.measureMemoryUsage(rowCount);
    });

    // Generate report
    this.generateReport();
  }
}

// CLI interface
if (require.main === module) {
  const analyzer = new TablePerformanceAnalyzer();

  // Parse command line arguments
  const args = process.argv.slice(2);
  const options = {};

  args.forEach(arg => {
    if (arg.startsWith('--rows=')) {
      const rows = arg.split('=')[1].split(',').map(Number);
      options.rowCounts = rows;
    } else if (arg.startsWith('--columns=')) {
      options.columnCount = Number(arg.split('=')[1]);
    }
  });

  // Run benchmark
  analyzer.runBenchmark(options);
}

module.exports = TablePerformanceAnalyzer;