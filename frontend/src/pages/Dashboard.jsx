import { useEffect, useState } from "react";
import api from "../api/api";
import PropertyCard from "../components/PropertyCard";
import TaskCard from "../components/TaskCard";

export default function Dashboard() {
  const [properties, setProperties] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");

  const load = async () => {
    const p = await api.get("/properties");
    setProperties(p.data);
    const t = await api.get("/tasks");
    setTasks(t.data);
  };

  useEffect(() => {
    load();
  }, []);

  const addProperty = async (e) => {
    e.preventDefault();
    await api.post("/properties", { name, address });
    setName("");
    setAddress("");
    load();
  };

  return (
    <div className="p-6 space-y-6">
      <section>
        <h1 className="text-xl font-semibold mb-2">Your Properties</h1>
        <form
          onSubmit={addProperty}
          className="flex flex-wrap gap-2 mb-4 text-sm"
        >
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Property name"
            className="px-3 py-2 rounded bg-slate-900 border border-slate-700"
            required
          />
          <input
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder="Address"
            className="px-3 py-2 rounded bg-slate-900 border border-slate-700"
            required
          />
          <button
            type="submit"
            className="px-4 py-2 rounded bg-emerald-500 text-slate-950 font-semibold"
          >
            Add
          </button>
        </form>
        <div className="grid gap-3 md:grid-cols-3">
          {properties.map((p) => (
            <PropertyCard key={p.id} property={p} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">Recent Tasks</h2>
        <div className="grid gap-2 md:grid-cols-2">
          {tasks.slice(0, 6).map((t) => (
            <TaskCard key={t.id} task={t} />
          ))}
        </div>
      </section>
    </div>
  );
}
