# Office Document Viewer

Display Word, Excel, and PowerPoint files in the browser.

## Microsoft Office Online Viewer

```tsx
function OfficeViewer({ fileUrl }: { fileUrl: string }) {
  const viewerUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(fileUrl)}`;

  return (
    <iframe
      src={viewerUrl}
      width="100%"
      height="600px"
      frameBorder="0"
    />
  );
}
```

**Supports:** .docx, .xlsx, .pptx (must be publicly accessible)

## Google Docs Viewer

```tsx
const googleViewerUrl = `https://docs.google.com/gview?url=${encodeURIComponent(fileUrl)}&embedded=true`;

<iframe src={googleViewerUrl} width="100%" height="600px" />
```

## Mammoth.js (Word to HTML)

```tsx
import mammoth from 'mammoth';

async function convertWordToHTML(file: File): Promise<string> {
  const arrayBuffer = await file.arrayBuffer();
  const result = await mammoth.convertToHtml({ arrayBuffer });
  return result.value;
}

function WordViewer({ file }: { file: File }) {
  const [html, setHtml] = useState('');

  useEffect(() => {
    convertWordToHTML(file).then(setHtml);
  }, [file]);

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
```

## Best Practices

1. **File must be publicly accessible** - For online viewers
2. **Fallback to download** - If viewing fails
3. **Loading state** - iframe takes time to load
4. **Error handling** - Unsupported file types

## Resources

- Mammoth.js: https://github.com/mwilliamson/mammoth.js
- Microsoft Office Viewer: https://support.microsoft.com/en-us/office/
