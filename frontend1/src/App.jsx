import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Feedback } from './pages/Feedback';
import { Auth } from './pages/Auth';

// Redirect unauthenticated users to /auth
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.auth?.isAuthenticated);
  return isAuthenticated ? children : <Navigate to="/auth" replace />;
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
        <Routes>
          {/* Auth page — no navbar */}
          <Route path="/auth" element={<Auth />} />

          {/* Protected pages — with navbar */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/feedback" element={<Feedback />} />
                  </Routes>
                </>
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
