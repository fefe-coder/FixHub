import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import useAuth from "../hooks/useAuth";

export default function Login() {
  const { setToken } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      const url = mode === "login" ? "/auth/login" : "/auth/register";
      const res = await api.post(url, { email, password });
      setToken(res.data.access_token);
      navigate("/");
    } catch (err) {
      alert("Failed: " + (err.response?.data?.detail || "Error"));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="w-full max-w-md bg-slate-950 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-semibold mb-4 text-center text-emerald-400">
          FixHub
        </h1>
        <p className="text-slate-400 text-center mb-6 text-sm">
          Property maintenance in one clean dashboard.
        </p>
        <form onSubmit={submit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 focus:outline-none focus:border-emerald-400 text-sm"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 focus:outline-none focus:border-emerald-400 text-sm"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="submit"
            className="w-full py-2 rounded bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm"
          >
            {mode === "login" ? "Log in" : "Create account"}
          </button>
        </form>
        <button
          className="mt-4 w-full text-xs text-slate-500"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login"
            ? "Need an account? Register"
            : "Already have an account? Log in"}
        </button>
      </div>
    </div>
  );
}
