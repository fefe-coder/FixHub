import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/api";
import TaskCard from "../components/TaskCard";

export default function PropertyDetail() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");

  const load = async () => {
    const p = await api.get(`/properties/${id}`);
    setProperty(p.data);
    const t = await api.get(`/tasks/property/${id}`);
    setTasks(t.data);
  };

  useEffect(() => {
    load();
  }, [id]);

  const addTask = async (e) => {
    e.preventDefault();
    await api.post("/tasks", {
      title,
      description: desc,
      property_id: Number(id),
    });
    setTitle("");
    setDesc("");
    load();
  };

  if (!property) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">{property.name}</h1>
        <p className="text-slate-400 text-sm">{property.address}</p>
      </div>

      <form onSubmit={addTask} className="space-y-2 max-w-md text-sm">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task title"
          className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700"
          required
        />
        <textarea
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          placeholder="Description"
          className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700"
        />
        <button
          type="submit"
          className="px-4 py-2 rounded bg-emerald-500 text-slate-950 font-semibold"
        >
          Add task
        </button>
      </form>

      <div className="grid gap-2 md:grid-cols-2">
        {tasks.map((t) => (
          <TaskCard key={t.id} task={t} />
        ))}
      </div>

      <a
        href={`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/reports/property/${id}`}
        target="_blank"
        className="inline-block mt-4 text-xs text-emerald-400 underline"
      >
        Download PDF report
      </a>
    </div>
  );
}
