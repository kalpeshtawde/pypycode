import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-16">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <img src="/logo.svg" alt="PyPyCode" className="w-8 h-8" />
              <span className="font-display font-semibold text-slate-900">PyPyCode</span>
            </div>
            <p className="text-slate-600 text-sm">
              A focused coding platform for Python developers.
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-semibold text-slate-900 mb-4">Product</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/problems" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  Problems
                </Link>
              </li>
              <li>
                <Link to="/leaderboard" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  Leaderboard
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold text-slate-900 mb-4">Legal</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/terms" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  Terms & Conditions
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-semibold text-slate-900 mb-4">Contact</h4>
            <ul className="space-y-2">
              <li>
                <a href="mailto:support@pypycode.com" className="text-slate-600 hover:text-emerald-600 text-sm transition-colors">
                  support@pypycode.com
                </a>
              </li>
              <li>
                <p className="text-slate-600 text-sm">
                  ISHA Systems LLC
                </p>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-slate-200 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-slate-600 text-sm">
            © 2026 ISHA Systems LLC. All rights reserved.
          </p>
          <p className="text-slate-600 text-sm mt-4 md:mt-0">
            PyPyCode - Python Problem Solving Platform
          </p>
        </div>
      </div>
    </footer>
  );
}
