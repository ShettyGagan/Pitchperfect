import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../store/authSlice';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Mic, Sparkles, Eye, EyeOff, ArrowRight, Zap } from 'lucide-react';

const API = 'http://127.0.0.1:8000';

export const Auth = () => {
  const [tab, setTab] = useState('login'); // 'login' | 'register'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const resetForm = () => {
    setEmail('');
    setPassword('');
    setError('');
    setShowPassword(false);
  };

  const handleTabSwitch = (newTab) => {
    setTab(newTab);
    resetForm();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setIsLoading(true);
    try {
      const endpoint = tab === 'login' ? '/auth/login' : '/auth/register';
      const { data } = await axios.post(`${API}${endpoint}`, { email, password });

      dispatch(setCredentials({
        token: data.access_token,
        user: { email },
      }));

      navigate('/');
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Something went wrong.';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="flex flex-col items-center mb-10">
          <div className="relative mb-4">
            <div className="bg-gradient-to-br from-violet-600 to-indigo-700 p-3 rounded-2xl shadow-xl shadow-violet-500/20">
              <Mic className="w-7 h-7 text-white" />
            </div>
            <div className="absolute -top-1 -right-1">
              <Sparkles className="w-4 h-4 text-amber-400 fill-current" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">SpeechPro</h1>
          <p className="text-sm text-slate-500 mt-1">AI Presentation Trainer</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-200/60 overflow-hidden">

          {/* Tab switcher */}
          <div className="flex border-b border-slate-100">
            {['login', 'register'].map((t) => (
              <button
                key={t}
                onClick={() => handleTabSwitch(t)}
                className={`flex-1 py-4 text-sm font-semibold transition-all duration-200 ${
                  tab === t
                    ? 'text-violet-700 border-b-2 border-violet-600 bg-violet-50/50'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                {t === 'login' ? 'Sign In' : 'Create Account'}
              </button>
            ))}
          </div>

          {/* Form */}
          <div className="p-8">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-slate-900">
                {tab === 'login' ? 'Welcome back' : 'Get started'}
              </h2>
              <p className="text-sm text-slate-500 mt-1">
                {tab === 'login'
                  ? 'Sign in to access your dashboard'
                  : 'Create an account to start training'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5" htmlFor="auth-email">
                  Email address
                </label>
                <input
                  id="auth-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500/30 focus:border-violet-400 transition-all duration-200"
                />
              </div>

              {/* Password */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-sm font-medium text-slate-700" htmlFor="auth-password">
                    Password
                  </label>
                  {tab === 'login' && (
                    <span className="text-xs text-violet-600 cursor-pointer hover:text-violet-700 font-medium">
                      Forgot password?
                    </span>
                  )}
                </div>
                <div className="relative">
                  <input
                    id="auth-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder={tab === 'register' ? 'Min. 6 characters' : '••••••••'}
                    autoComplete={tab === 'login' ? 'current-password' : 'new-password'}
                    className="w-full px-4 py-3 pr-12 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500/30 focus:border-violet-400 transition-all duration-200"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="bg-red-50 border border-red-200/60 rounded-xl px-4 py-3">
                  <p className="text-sm text-red-600 font-medium">{error}</p>
                </div>
              )}

              {/* Submit */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-slate-900 to-slate-800 text-white py-3 rounded-xl font-semibold text-sm hover:from-slate-800 hover:to-slate-700 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-slate-900/20 flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    {tab === 'login' ? 'Signing in…' : 'Creating account…'}
                  </>
                ) : (
                  <>
                    {tab === 'login' ? 'Sign In' : 'Create Account'}
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-3 my-6">
              <div className="flex-1 h-px bg-slate-100" />
              <span className="text-xs text-slate-400 font-medium">or</span>
              <div className="flex-1 h-px bg-slate-100" />
            </div>

            {/* Switch tab prompt */}
            <p className="text-center text-sm text-slate-500">
              {tab === 'login' ? "Don't have an account? " : 'Already have an account? '}
              <button
                onClick={() => handleTabSwitch(tab === 'login' ? 'register' : 'login')}
                className="text-violet-600 font-semibold hover:text-violet-700 transition-colors"
              >
                {tab === 'login' ? 'Sign up free' : 'Sign in'}
              </button>
            </p>
          </div>
        </div>

        {/* Feature hint */}
        <div className="mt-6 flex items-center justify-center gap-6">
          {['AI Analysis', 'Voice Metrics', 'Smart Feedback'].map((label, i) => (
            <div key={i} className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
              <Zap className="w-3 h-3 text-violet-400" />
              {label}
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};
