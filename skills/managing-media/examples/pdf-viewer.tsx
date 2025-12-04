import React, { useState } from 'react';
import { Document, Page } from 'react-pdf';

/**
 * Simple PDF Viewer
 *
 * Minimal PDF viewer with page navigation
 */

export function SimplePDFViewer({ url }: { url: string }) {
  const [numPages, setNumPages] = useState(0);
  const [page, setPage] = useState(1);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-bold">PDF Viewer</h2>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            ← Prev
          </button>

          <span className="text-sm">
            {page} / {numPages}
          </span>

          <button
            onClick={() => setPage(p => Math.min(numPages, p + 1))}
            disabled={page === numPages}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Next →
          </button>
        </div>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <Document
          file={url}
          onLoadSuccess={({ numPages }) => setNumPages(numPages)}
        >
          <Page pageNumber={page} width={800} />
        </Document>
      </div>
    </div>
  );
}

export default SimplePDFViewer;
