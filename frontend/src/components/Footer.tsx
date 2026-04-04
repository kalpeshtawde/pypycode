import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-16">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Reddit+Sans:wght@700;800&display=swap');
        
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
        
        .footer-logo-icon {
          width: 32px;
          height: 32px;
          border-radius: 7px;
          background: #0F172A;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          position: relative;
        }
        
        .footer-logo-prompt {
          font-family: "Reddit Sans", monospace;
          font-size: 14px;
          font-weight: 700;
          color: #1A6BFF;
          position: absolute;
          left: 5px;
          top: 50%;
          transform: translateY(-50%);
          line-height: 1;
        }
        
        .footer-logo-cursor {
          width: 5px;
          height: 9px;
          background: #6366F1;
          border-radius: 1px;
          position: absolute;
          right: 6px;
          top: 50%;
          transform: translateY(-50%);
          animation: blink 1.2s ease-in-out infinite;
        }
        
        .footer-logo-wordmark {
          font-size: 19px;
          font-weight: 800;
          line-height: 1;
          letter-spacing: -0.3px;
          display: inline-flex;
          align-items: baseline;
        }
        
        .footer-logo-blue {
          color: #1A6BFF;
          font-size: 19px;
          font-weight: 800;
        }
        
        .footer-logo-dark {
          color: #0F172A;
          font-size: 19px;
          font-weight: 800;
        }
      `}</style>
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              {/* Icon */}
              <div className="footer-logo-icon">
                <span className="footer-logo-prompt">&gt;_</span>
                <div className="footer-logo-cursor"></div>
              </div>
              
              {/* Wordmark */}
              <span className="footer-logo-wordmark">
                <span className="footer-logo-blue">PyPy</span>
                <span className="footer-logo-dark">Code</span>
              </span>
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
