import { useRef, useState } from "react";
import { Upload, FileJson } from "lucide-react";
import toast from "react-hot-toast";

import { uploadFile } from "../../api/api";

export default function UploadSection({ onUploadSuccess }) {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      await uploadFile(formData);

      toast.success("Billing file uploaded successfully.");

      setFile(null);
      inputRef.current.value = "";

      if (onUploadSuccess) {
        await onUploadSuccess();
      }
    } catch (err) {
      console.error(err);
      toast.error("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      className="mb-8 rounded-xl border p-6"
      style={{
        background: "#FCFDFE",
        borderColor: "#D6E6F8",
        boxShadow: "0 2px 8px rgba(15,23,42,.04)",
      }}
    >
      <div className="flex items-center gap-3 mb-5">
        <Upload size={22} color="#2D5FD4" />

        <div>
          <h2 className="text-lg font-semibold">
            Upload Billing JSON
          </h2>

          <p className="text-sm text-slate-500">
            Upload today's billing file to refresh the dashboard.
          </p>
        </div>
      </div>

      <div className="flex flex-col gap-4 md:flex-row md:items-center">

        <label
          className="
            flex
            cursor-pointer
            items-center
            gap-3
            rounded-lg
            border
            border-dashed
            border-slate-300
            bg-slate-50
            px-5
            py-4
            flex-1
          "
        >
          <FileJson size={22} />

          <span className="truncate">
            {file ? file.name : "Choose JSON file"}
          </span>

          <input
            ref={inputRef}
            type="file"
            accept=".json"
            hidden
            onChange={(e) =>
              setFile(e.target.files[0])
            }
          />
        </label>

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="
            rounded-lg
            bg-blue-600
            px-6
            py-3
            font-medium
            text-white
            hover:bg-blue-700
            disabled:cursor-not-allowed
            disabled:bg-slate-300
          "
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>

      </div>
    </div>
  );
}