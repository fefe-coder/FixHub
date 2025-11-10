import { Link } from "react-router-dom";

export default function TaskCard({ task }) {
  return (
    <Link
      to={`/tasks/${task.id}`}
      className="p-3 bg-slate-800 rounded-lg border border-slate-700 hover:border-emerald-400 transition flex justify-between items-center"
    >
      <div>
        <h3 className="font-medium">{task.title}</h3>
        <p className="text-xs text-slate-400">
          Status: <span className="text-emerald-400">{task.status}</span>
        </p>
      </div>
      <span className="text-xs text-slate-500">
        {task.assigned_to || "Unassigned"}
      </span>
    </Link>
  );
}
