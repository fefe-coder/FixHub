import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("fixhub_token");
    navigate("/login");
  };

  return (
    <nav className="w-full flex items-center justify-between px-6 py-3 bg-slate-950 border-b border-slate-800">
      <Link to="/" className="text-xl font-semibold text-emerald-400">
        FixHub
      </Link>
      <button
        onClick={logout}
        className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sm"
      >
        Logout
      </button>
    </nav>
  );
}
