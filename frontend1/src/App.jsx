import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Feedback } from './pages/Feedback';

function App() {
  return (
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/feedback" element={<Feedback />} />
          </Routes>
        </div>
      </Router>
    );
}

export default App
