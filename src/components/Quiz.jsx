import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, CheckCircle2, XCircle, Code, Award, Zap } from 'lucide-react';

const Quiz = () => {
  const [questions, setQuestions] = useState([]);
  const [step, setStep] = useState(0);
  const [choice, setChoice] = useState('');
  const [status, setStatus] = useState('idle'); // 'idle', 'correct', 'wrong', 'finished'
  const [loading, setLoading] = useState(true);
  const [hasAnswered, setHasAnswered] = useState(false);
    const [isCorrect, setIsCorrect] = useState(null);
    const [selectedChoice, setSelectedChoice] = useState("");

  useEffect(() => {
    // Appel vers ton API FastAPI
    setLoading(true);
    axios.get('http://localhost:8000/questions/random?limit=30')
      .then(res => {
        setQuestions(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur Backend :", err);
        setLoading(false);
      });
  }, []);

  const handleCheck = () => {
    const q = questions[step];
    let isCorrect = false;

    if (q.choix_multiple) {
      isCorrect = choice === q.solution;
    } else {
      // Normalisation simple : minuscules, trim et suppression des espaces autour des parenthèses/points
      const cleanInput = choice.trim().toLowerCase().replace(/\s*([.()])\s*/g, '$1');
      const cleanSol = q.solution.trim().toLowerCase().replace(/\s*([.()])\s*/g, '$1');
      isCorrect = cleanInput === cleanSol;
    }
    setStatus(isCorrect ? 'correct' : 'wrong');
  };

  const handleNext = () => {
    setChoice('');
    setStatus('idle');
    if (step < questions.length - 1) {
      setStep(s => s + 1);
    } else {
      setStatus('finished');
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <div className="w-12 h-12 border-4 border-slate-200 border-t-blue-500 rounded-full animate-spin"></div>
      <p className="text-slate-500 font-bold">Chargement du défi...</p>
    </div>
  );
  
  if (status === 'finished' || questions.length === 0) return (
    <motion.div initial={{scale: 0.9, opacity: 0}} animate={{scale: 1, opacity: 1}} className="text-center p-12 bg-white rounded-3xl shadow-xl border-2 border-slate-100 max-w-lg mx-auto">
      <Award className="mx-auto text-yellow-400 mb-6" size={80} strokeWidth={1} />
      <h2 className="text-4xl font-black text-green-600 tracking-tighter mb-4">LEÇON TERMINÉE !</h2>
      <p className="text-slate-600 text-lg mb-8">Bravo ! Tu as validé 30 requêtes MongoDB. Tu es sur la voie de l'expertise ! 🏆</p>
      <button onClick={() => window.location.reload()} className="bg-green-500 text-white w-full py-4 rounded-2xl font-black shadow-[0_5px_0_0_#22c55e] hover:bg-green-400">RECOMMENCER</button>
    </motion.div>
  );

  const q = questions[step];
  const totalSteps = questions.length;

  return (
    <div className="max-w-3xl mx-auto pb-32"> {/* PB-32 pour la barre de feedback du bas */}
      {/* Barre de Progression Style Duolingo */}
      <div className="w-full bg-slate-200 h-5 rounded-full overflow-hidden mb-12 flex items-center p-1 shadow-inner">
        <motion.div 
          className="bg-green-500 h-3 rounded-full shadow" 
          initial={{ width: 0 }}
          animate={{ width: `${((step + 1) / totalSteps) * 100}%` }}
          transition={{ duration: 0.5 }}
        />
        <span className="absolute right-8 text-xs font-bold text-slate-400">{step + 1} / {totalSteps}</span>
      </div>

      <AnimatePresence mode='wait'>
        <motion.div 
          key={step} 
          initial={{ x: 50, opacity: 0 }} 
          animate={{ x: 0, opacity: 1 }} 
          exit={{ x: -50, opacity: 0 }} 
          className="bg-white p-8 md:p-10 rounded-3xl border-2 border-slate-100 shadow-xl"
        >
          {/* Header de la question */}
          <div className="flex justify-between items-center mb-6 pb-4 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Zap className={`p-2 rounded-lg ${q.difficulte === 'Facile' ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'}`} size={36}/>
              <h3 className="text-xl font-extrabold text-slate-900 leading-tight">Niveau : {q.difficulte}</h3>
            </div>
            <div className={`px-4 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider ${q.choix_multiple ? 'bg-blue-50 text-blue-600' : 'bg-purple-50 text-purple-600'}`}>
              {q.choix_multiple ? "QCM" : "Syntaxe"}
            </div>
          </div>

          {/* Énoncé (Correction : On s'assure qu'il est bien visible) */}
          <p className="text-slate-600 text-sm font-bold uppercase tracking-widest mb-1 ml-1">ÉNONCÉ :</p>
          <h2 className="text-2xl md:text-3xl font-black text-slate-900 tracking-tight leading-snug mb-10">
            {q.enonce || "L'énoncé de la question est manquant."}
          </h2>

          {/* Corps de la réponse */}
          {q.choix_multiple ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {q.propositions && q.propositions.map((p, i) => (
                <button
                  key={i}
                  disabled={status !== 'idle'}
                  onClick={() => setChoice(p)}
                  className={`relative p-5 rounded-2xl border-2 text-left transition-all font-mono text-sm leading-relaxed group ${
                    choice === p ? 'border-blue-400 bg-blue-50 shadow-[0_5px_0_0_#60a5fa]' : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  } ${status !== 'idle' && p === q.solution ? 'border-green-500 bg-green-50' : status === 'wrong' && choice === p ? 'border-red-400 bg-red-50' : ''}`}
                >
                    <span className={`absolute left-4 top-1/2 -translate-y-1/2 font-sans font-black text-lg ${choice === p ? 'text-blue-500' : 'text-slate-300'}`}>{i+1}</span>
                    <span className="pl-8">{p}</span>
                </button>
              ))}
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              <label className="text-lg font-extrabold text-slate-700 flex items-center gap-2">
                <Code className="text-purple-500"/> Tape ta requête MongoDB :
              </label>
              <textarea
                value={choice}
                disabled={status !== 'idle'}
                onChange={(e) => setChoice(e.target.value)}
                rows={3}
                placeholder="db.collection.find({ ... })"
                className={`w-full p-5 rounded-2xl border-2 font-mono text-sm outline-none transition-all resize-none ${
                  status === 'idle' ? 'border-slate-200 focus:border-blue-400 focus:shadow-[0_5px_0_0_#60a5fa]' : 
                  status === 'correct' ? 'border-green-500 bg-green-50 shadow-[0_5px_0_0_#22c55e]' : 'border-red-500 bg-red-50'
                }`}
              />
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Barre de Feedback Fixe en Bas Style Duolingo */}
      <div className={`fixed bottom-0 left-0 w-full p-6 transition-colors border-t-2 ${
        status === 'idle' ? 'bg-white border-slate-200' : status === 'correct' ? 'bg-green-100 border-green-200' : 'bg-red-100 border-red-200'
      }`}>
        <div className="max-w-3xl mx-auto flex items-center justify-between gap-6">
          <div className="flex-1">
            <AnimatePresence>
              {status !== 'idle' && (
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
                  <div className="flex items-center gap-3 mb-1.5">
                    {status === 'correct' ? <CheckCircle2 className="text-green-600" size={32} /> : <XCircle className="text-red-600" size={32} />}
                    <h3 className={`font-black text-2xl tracking-tighter ${status === 'correct' ? 'text-green-700' : 'text-red-700'}`}>
                      {status === 'correct' ? 'Excellent !' : 'Dommage !'}
                    </h3>
                  </div>
                    <div className="ml-11 max-w-xl">
                    {/* Affichage de la solution si erreur */}
                    {status === 'wrong' && (
                        <div className="mb-2">
                        <span className="text-xs font-black uppercase text-red-400 tracking-widest block">La bonne réponse était :</span>
                        <code className="bg-red-200 text-red-900 px-2 py-1 rounded text-sm font-mono font-bold">
                            {q.solution}
                        </code>
                        </div>
                    )}

                    {/* L'explication reste présente en dessous */}
                    <p className={`text-sm italic font-medium ${status === 'correct' ? 'text-green-700' : 'text-red-700 opacity-80'}`}>
                        💡 {q.explication || "Pas d'explication disponible."}
                    </p>
                    </div>                
                </motion.div>
              )}
            </AnimatePresence>
          </div>
          
          <div className="flex-shrink-0">
            {status === 'idle' ? (
              <button 
                onClick={handleCheck} 
                disabled={!choice} 
                className="bg-green-500 text-white px-12 py-4 rounded-2xl font-black text-lg shadow-[0_5px_0_0_#22c55e] hover:bg-green-400 hover:shadow-[0_4px_0_0_#22c55e] disabled:opacity-40 disabled:cursor-not-allowed transform hover:-translate-y-0.5"
              >
                VÉRIFIER
              </button>
            ) : (
              <button 
                onClick={handleNext} 
                className={`text-white px-12 py-4 rounded-2xl font-black text-lg shadow-[0_5px_0_0] transform hover:-translate-y-0.5 ${
                  status === 'correct' ? 'bg-blue-500 shadow-#3b82f6 hover:bg-blue-400' : 'bg-red-500 shadow-#ef4444 hover:bg-red-400'
                }`}
              >
                CONTINUER
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Quiz;