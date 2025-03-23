"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, ImageIcon, RefreshCw } from "lucide-react";

export default function ImageUpload() {
  const [image, setImage] = useState<string | null>(null);
  const [caption, setCaption] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => setImage(e.target?.result as string);
    reader.readAsDataURL(file);

    setCaption(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("API Response:", data); // This will show in the browser console
      
      if (data.caption) {
        setCaption(data.caption);
      } else {
        setCaption("Failed to generate caption. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      setCaption("Failed to generate caption. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleNewImage = () => {
    setImage(null);
    setCaption(null);
  };

  return (
    <section id="image-upload" className="py-20 bg-gray-900">
      <div className="container mx-auto px-6">
        <h2 className="text-3xl md:text-4xl font-bold mb-8 text-center text-white">
          Upload Your Image
        </h2>
        <div className="max-w-2xl mx-auto bg-gray-800 p-8 rounded-lg shadow-lg">
          <div className="mb-6">
            <Input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" id="image-input" />
            <label
              htmlFor="image-input"
              className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-600 border-dashed rounded-lg cursor-pointer hover:border-purple-500 transition duration-300 ease-in-out"
            >
              {image ? (
                <img
                  src={image || "/placeholder.svg"}
                  alt="Uploaded"
                  className="w-full h-full object-contain rounded-lg"
                />
              ) : (
                <div className="flex flex-col items-center justify-center pt-7">
                  <Upload className="w-12 h-12 text-gray-400" />
                  <p className="mt-2 text-sm text-gray-400">Drag and drop or click to upload</p>
                </div>
              )}
            </label>
          </div>
          {loading && <p className="text-center text-white">Generating caption...</p>}
          {caption && (
            <div className="mt-6 p-4 bg-gray-700 rounded-lg">
              <h3 className="text-xl font-semibold mb-2 flex items-center text-white">
                <ImageIcon className="mr-2" /> Generated Caption
              </h3>
              <p className="text-gray-300 mb-4">{caption}</p>
              <Button
                onClick={handleNewImage}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition duration-300 ease-in-out transform hover:scale-105"
              >
                <RefreshCw className="mr-2 h-4 w-4" /> Select New Image
              </Button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
