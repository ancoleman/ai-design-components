import React, { useState } from 'react';
import Cropper from 'react-easy-crop';
import { Point, Area } from 'react-easy-crop/types';

/**
 * Image Upload with Cropping
 *
 * Features: File upload, image preview, crop tool, zoom controls
 * Library: react-easy-crop
 * Install: npm install react-easy-crop
 */

export function ImageUploadWithCrop() {
  const [image, setImage] = useState<string | null>(null);
  const [crop, setCrop] = useState<Point>({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedArea, setCroppedArea] = useState<Area | null>(null);

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => setImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const onCropComplete = (croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedArea(croppedAreaPixels);
  };

  return (
    <div className="p-4">
      <input type="file" accept="image/*" onChange={onFileChange} className="mb-4" />

      {image && (
        <div>
          <div className="relative h-96 bg-gray-100">
            <Cropper
              image={image}
              crop={crop}
              zoom={zoom}
              aspect={1}  // Square crop
              onCropChange={setCrop}
              onZoomChange={setZoom}
              onCropComplete={onCropComplete}
            />
          </div>

          <div className="mt-4 flex items-center gap-4">
            <label className="flex items-center gap-2">
              Zoom:
              <input
                type="range"
                min={1}
                max={3}
                step={0.1}
                value={zoom}
                onChange={(e) => setZoom(Number(e.target.value))}
              />
            </label>

            <button className="px-4 py-2 bg-blue-500 text-white rounded">
              Save Cropped Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageUploadWithCrop;
