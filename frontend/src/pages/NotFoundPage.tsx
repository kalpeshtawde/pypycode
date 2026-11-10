import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useSEO } from "../hooks/useSEO";
import { getNotFoundMetadata } from "../utils/seo";

export default function NotFoundPage() {
  useSEO(useMemo(() => getNotFoundMetadata(), []));

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50 py-24">
      <div className="max-w-xl mx-auto px-6 text-center">
        <p className="text-sm font-semibold tracking-wide text-emerald-600 mb-3">404</p>
        <h1 className="font-display text-4xl font-bold text-slate-900 mb-4">Page not found</h1>
        <p className="text-slate-600 mb-10">
          The page you are looking for does not exist or may have been moved.
        </p>
        <div className="flex items-center justify-center gap-3">
          <Link to="/" className="btn-primary inline-flex text-base px-6 py-3">
            Go home
          </Link>
          <Link
            to="/problems"
            className="inline-flex px-6 py-3 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold hover:bg-slate-50 transition-colors"
          >
            Browse problems
          </Link>
        </div>
      </div>
    </div>
  );
}
