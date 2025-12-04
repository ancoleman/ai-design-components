import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

/**
 * PDF Viewer with react-pdf
 *
 * Features: Page navigation, zoom, thumbnail sidebar
 * Install: npm install react-pdf pdfjs-dist
 */

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export function PDFViewer({ file }: { file: string }) {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);

  return (
    <div className="flex h-screen">
      {/* Thumbnail sidebar */}
      <div className="w-48 border-r overflow-y-auto bg-gray-50 p-2">
        <Document file={file} onLoadSuccess={() => {}}>
          {Array.from({ length: numPages }, (_, i) => (
            <div
              key={i}
              onClick={() => setPageNumber(i + 1)}
              className={`mb-2 cursor-pointer border-2 ${
                pageNumber === i + 1 ? 'border-blue-500' : 'border-transparent'
              }`}
            >
              <Page pageNumber={i + 1} width={160} renderTextLayer={false} renderAnnotationLayer={false} />
              <p className="text-xs text-center mt-1">{i + 1}</p>
            </div>
          ))}
        </Document>
      </div>

      {/* Main viewer */}
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
              disabled={pageNumber === 1}
              className="px-3 py-1 border rounded disabled:opacity-50"
            >
              Previous
            </button>

            <span className="text-sm">
              Page {pageNumber} of {numPages}
            </span>

            <button
              onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
              disabled={pageNumber === numPages}
              className="px-3 py-1 border rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button onClick={() => setScale(Math.max(0.5, scale - 0.1))}>-</button>
            <span className="text-sm">{Math.round(scale * 100)}%</span>
            <button onClick={() => setScale(Math.min(2, scale + 0.1))}>+</button>
          </div>
        </div>

        <div className="flex-1 overflow-auto p-4 flex justify-center">
          <Document
            file={file}
            onLoadSuccess={({ numPages }) => setNumPages(numPages)}
          >
            <Page pageNumber={pageNumber} scale={scale} />
          </Document>
        </div>
      </div>
    </div>
  );
}

export default PDFViewer;
