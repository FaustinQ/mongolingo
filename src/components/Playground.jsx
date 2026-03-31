import React, { useState } from 'react';
import axios from 'axios';
import { Terminal, Play, Database, AlertCircle, CheckCircle2 } from 'lucide-react';

const Playground = () => {
  const [query, setQuery] = useState("db.WaterPoints.find({'insee5': 56000}).limit(5)");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const executeQuery = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post('http://localhost:8000/sandbox/run', { query });
      if (res.data.success) {
        setResult(res.data.result);
      } else {
        setError(res.data.error);
      }
    } catch (err) {
      setError("Le serveur ne répond pas. Vérifie ton Backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-180px)] gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-black text-slate-900 flex items-center gap-3">
            <Terminal className="text-blue-500" size={32} /> Playground MongoDB
          </h2>
          <p className="text-slate-500 font-medium">Exécute tes propres requêtes PyMongo sur la collection WaterPoints.</p>
        </div>
        <button 
          onClick={executeQuery}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-400 text-white px-8 py-4 rounded-2xl font-black shadow-[0_5px_0_0_#2563eb] transition-all flex items-center gap-2 active:translate-y-1 active:shadow-none"
        >
          {loading ? "EXÉCUTION..." : <><Play size={20} fill="currentColor" /> LANCER LA REQUÊTE</>}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 overflow-hidden">
        {/* ÉDITEUR DE CODE */}
        <div className="bg-slate-900 rounded-3xl p-6 flex flex-col shadow-2xl border-4 border-slate-800">
          <div className="flex items-center gap-2 mb-4 text-slate-400 text-xs font-bold uppercase tracking-widest">
            <Database size={14} /> Console de commande
          </div>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-green-400 font-mono text-lg outline-none resize-none spellcheck-false"
            spellCheck="false"
          />
        </div>

        {/* RÉSULTATS */}
        <div className="bg-white rounded-3xl border-2 border-slate-200 flex flex-col shadow-sm overflow-hidden">
          <div className="p-4 border-b-2 border-slate-100 bg-slate-50 flex justify-between items-center">
            <span className="font-black text-slate-400 text-xs uppercase tracking-widest">Résultat de la collection</span>
            {result && <span className="text-[10px] bg-green-100 text-green-600 px-2 py-1 rounded-lg font-bold">JSON VALIDATED</span>}
          </div>
          
          <div className="flex-1 p-6 overflow-auto font-mono text-sm bg-slate-50">
            {error && (
              <div className="flex items-start gap-3 text-red-600 bg-red-50 p-4 rounded-xl border border-red-100 animate-pulse">
                <AlertCircle size={20} />
                <p className="font-bold">{error}</p>
              </div>
            )}
            
            {result ? (
              <pre className="text-slate-800 italic">
                {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
              </pre>
            ) : !error && (
              <div className="h-full flex flex-col items-center justify-center text-slate-300">
                <Database size={48} strokeWidth={1} className="mb-2" />
                <p className="font-bold italic underline decoration-blue-200">En attente d'une commande...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;