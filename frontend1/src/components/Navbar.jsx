import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Mic, BarChart3, Sparkles } from 'lucide-react';

export const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="bg-white/95 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3">
            <div className="relative">
              <div className="bg-gradient-to-br from-violet-600 to-indigo-700 p-2.5 rounded-xl shadow-lg">
                <Mic className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -top-1 -right-1">
                <Sparkles className="w-3 h-3 text-amber-400 fill-current" />
              </div>
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                SpeechPro
              </span>
              <div className="text-xs text-slate-500 font-medium -mt-1">AI Platform</div>
            </div>
          </Link>
          
          <div className="flex items-center space-x-1">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                location.pathname === '/'
                  ? 'bg-slate-900 text-white shadow-lg shadow-slate-900/25'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Upload
            </Link>
            <Link
              to="/feedback"
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 ${
                location.pathname === '/feedback'
                  ? 'bg-slate-900 text-white shadow-lg shadow-slate-900/25'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Analytics</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};