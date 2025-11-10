import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PropertyDetail from "./pages/PropertyDetail";
import TaskDetail from "./pages/TaskDetail";
import Navbar from "./components/Navbar";
import useAuth from "./hooks/useAuth";

export default function App() {
  const { token } = useAuth();

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {token && <Navbar />}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={token ? <Dashboard /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/properties/:id"
          element={token ? <PropertyDetail /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/tasks/:id"
          element={token ? <TaskDetail /> : <Navigate to="/login" replace />}
        />
      </Routes>
    </div>
  );
}
