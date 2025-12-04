# PDF Viewer Implementation

Display PDFs in-browser with navigation, zoom, search, and annotations.

## Libraries

| Library | Features | Size | Best For |
|---------|----------|------|----------|
| **PDF.js** | Mozilla's, full-featured | 600KB | General purpose |
| **react-pdf** | React wrapper for PDF.js | 650KB | React apps |
| **PSPDFKit** | Enterprise, annotations | Commercial | Advanced features |

## react-pdf Basic

```tsx
import { Document, Page, pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PDFViewer({ file }: { file: string }) {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState(1);

  return (
    <div>
      <Document
        file={file}
        onLoadSuccess={({ numPages }) => setNumPages(numPages)}
      >
        <Page pageNumber={pageNumber} width={600} />
      </Document>

      <div className="controls">
        <button onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}>
          Previous
        </button>
        <span>Page {pageNumber} of {numPages}</span>
        <button onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}>
          Next
        </button>
      </div>
    </div>
  );
}
```

## Zoom and Pan

```tsx
function PDFViewerWithZoom({ file }: Props) {
  const [scale, setScale] = useState(1.0);

  return (
    <div>
      <div className="toolbar">
        <button onClick={() => setScale(s => Math.max(0.5, s - 0.1))}>-</button>
        <span>{Math.round(scale * 100)}%</span>
        <button onClick={() => setScale(s => Math.min(2.0, s + 0.1))}>+</button>
      </div>

      <Document file={file}>
        <Page pageNumber={1} scale={scale} />
      </Document>
    </div>
  );
}
```

## Text Search

```tsx
import { pdfjs } from 'react-pdf';

async function searchPDF(pdf: pdfjs.PDFDocumentProxy, query: string) {
  const results = [];

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const text = textContent.items.map((item: any) => item.str).join(' ');

    if (text.toLowerCase().includes(query.toLowerCase())) {
      results.push({ page: i, text });
    }
  }

  return results;
}
```

## Resources

- react-pdf: https://github.com/wojtekmaj/react-pdf
- PDF.js: https://mozilla.github.io/pdf.js/
