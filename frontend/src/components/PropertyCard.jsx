import { Link } from "react-router-dom";

export default function PropertyCard({ property }) {
  return (
    <Link
      to={`/properties/${property.id}`}
      className="p-4 bg-slate-800 rounded-xl border border-slate-700 hover:border-emerald-400 transition"
    >
      <h2 className="text-lg font-semibold">{property.name}</h2>
      <p className="text-slate-400 text-sm">{property.address}</p>
    </Link>
  );
}
