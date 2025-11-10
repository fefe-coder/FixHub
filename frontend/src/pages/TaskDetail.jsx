import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/api";

export default function TaskDetail() {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [status, setStatus] = useState("Pending");
  const [file, setFile] = useState(null);
  const [photoType, setPhotoType] = useState("before");

  const load = async () => {
    const res = await api.get(`/tasks/${id}`);
    setTask(res.data);
    setStatus(res.data.status);
  };

  useEffect(() => {
    load();
  }, [id]);

  const updateStatus = async () => {
    await api.put(`/tasks/${id}`, { status });
    load();
  };

  const uploadPhoto = async (e) => {
    e.preventDefault();
    if (!file) return;
    const form = new FormData();
    form.append("task_id", id);
    form.append("photo_type", photoType);
    form.append("file", file);
    await api.post("/uploads/task-photo", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setFile(null);
    load();
  };

  if (!task) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 space-y-4">
      <div>
        <h1 className="text-xl font-semibold">{task.title}</h1>
        <p className="text-slate-400 text-sm">{task.description}</p>
      </div>

      <div className="space-x-2 text-sm">
        <span>Status:</span>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="bg-slate-900 border border-slate-700 px-2 py-1 rounded"
        >
          <option>Pending</option>
          <option>In Progress</option>
          <option>Done</option>
        </select>
        <button
          onClick={updateStatus}
          className="px-3 py-1 bg-emerald-500 text-slate-950 rounded font-semibold"
        >
          Save
        </button>
      </div>

      <form
        onSubmit={uploadPhoto}
        className="space-y-2 max-w-sm text-xs bg-slate-950 p-3 rounded-lg border border-slate-800"
      >
        <div className="flex gap-2 items-center">
          <label>Photo type:</label>
          <select
            value={photoType}
            onChange={(e) => setPhotoType(e.target.value)}
            className="bg-slate-900 border border-slate-700 px-2 py-1 rounded"
          >
            <option value="before">Before</option>
            <option value="after">After</option>
          </select>
        </div>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="text-slate-300"
        />
        <button
          type="submit"
          className="px-3 py-1 bg-slate-800 hover:bg-slate-700 rounded"
        >
          Upload photo
        </button>
      </form>

      {task.photos && task.photos.length > 0 && (
        <div className="grid gap-2 grid-cols-2 mt-3">
          {task.photos.map((p) => (
            <div key={p.id} className="text-xs">
              <div className="mb-1 capitalize text-emerald-400">
                {p.photo_type}
              </div>
              <img
                src={p.url}
                alt={p.photo_type}
                className="w-full h-32 object-cover rounded border border-slate-700"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
