import React, { useState } from 'react';
import Quiz from './components/Quiz';
import Playground from './components/Playground';
import DataManager from './components/DataManager';
import { Layout, PlayCircle, Terminal, Database } from 'lucide-react';

const App = () => {
  // L'état qui définit l'onglet actif : 'quiz', 'playground' ou 'data'
  const [activeTab, setActiveTab] = useState('quiz');

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* HEADER / NAVIGATION */}
      <nav className="bg-white border-b-2 border-slate-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-xl">
              <Database className="text-white" size={24} />
            </div>
            <h1 className="text-2xl font-black tracking-tighter text-slate-800">
              MONGO<span className="text-blue-600">LINGO</span>
            </h1>
          </div>

          <div className="flex bg-slate-100 p-1.5 rounded-2xl gap-1">
            <TabButton 
              active={activeTab === 'quiz'} 
              onClick={() => setActiveTab('quiz')}
              icon={<PlayCircle size={18} />}
              label="Apprendre"
            />
            <TabButton 
              active={activeTab === 'playground'} 
              onClick={() => setActiveTab('playground')}
              icon={<Terminal size={18} />}
              label="Playground"
            />
            <TabButton 
              active={activeTab === 'data'} 
              onClick={() => setActiveTab('data')}
              icon={<Layout size={18} />}
              label="Données"
            />
          </div>
        </div>
      </nav>

      {/* CONTENU DYNAMIQUE */}
      <main className="max-w-6xl mx-auto p-8">
        {activeTab === 'quiz' && <Quiz />}
        {activeTab === 'playground' && <Playground />}
        {activeTab === 'data' && <DataManager />}
      </main>
    </div>
  );
};

// Petit composant interne pour les boutons de navigation (plus propre)
const TabButton = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold transition-all ${
      active 
        ? 'bg-white text-blue-600 shadow-sm ring-1 ring-slate-200' 
        : 'text-slate-500 hover:bg-slate-200'
    }`}
  >
    {icon}
    <span>{label}</span>
  </button>
);

export default App;