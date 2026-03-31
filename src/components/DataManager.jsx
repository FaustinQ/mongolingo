import React, { useState } from 'react';
import { FileCode, ShieldQuestion, RotateCcw, Download, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

const DataManager = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleReset = async () => {
    if (!window.confirm("⚠️ Attention : Cela va supprimer toutes les modifications et restaurer les données d'origine du Morbihan. Continuer ?")) return;

    setLoading(true);
    setMessage("");
    
    try {
      // On appelle la route reset qu'on va créer dans le backend
      const response = await axios.post('http://localhost:8000/sandbox/reset');
      if (response.data.success) {
        setMessage("Base restaurée avec succès ! ✅");
        // On efface le message après 3 secondes
        setTimeout(() => setMessage(""), 3000);
      }
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la réinitialisation : " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get('http://localhost:8000/sandbox/export');

      // Si le backend a renvoyé une erreur formatée en JSON au lieu du fichier
      if (response.data.success === false) {
        alert("Erreur: " + response.data.error);
        return;
      }

      // On transforme la réponse en Blob
      const dataString = typeof response.data === 'string' 
                        ? response.data 
                        : JSON.stringify(response.data, null, 2);
                        
      const blob = new Blob([dataString], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `backup_waterpoints_${new Date().getTime()}.json`;
      document.body.appendChild(link);
      link.click();
      
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'exportation.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Structure de la collection (ton bloc existant) */}
      <div className="bg-white p-8 rounded-3xl border-2 border-slate-200 shadow-sm">
        <h2 className="text-2xl font-black mb-6 flex items-center gap-3">
          <ShieldQuestion className="text-blue-500" /> Structure de la Collection
        </h2>
        <div className="bg-slate-900 text-green-400 p-6 rounded-xl font-mono text-sm overflow-x-auto shadow-inner">
          <p>// Collection: WaterPoints</p>
          <p>{"{"}</p>
          <p className="ml-4">"_id": ObjectId("..."),</p>
          <p className="ml-4">"location": {"{ \"type\": \"Point\", \"coordinates\": [lon, lat] }" },</p>
          <p className="ml-4">"date_crea": date,</p>
          <p className="ml-4">"date_maj": date,</p>
          <p className="ml-4">"utilisateur": string,</p>
          <p className="ml-4">"carto_ref": int,</p>
          <p className="ml-4">"statut": "PUBLIC" | "PRIVE",</p>
          <p className="ml-4">"press_debit": Double,</p>
          <p className="ml-4">"debit_1_bar": Double,</p>
          <p className="ml-4">"numero_pei": int,</p>
          <p className="ml-4">"insee5": Int</p>
          <p className="ml-4">"type_nature": string,</p>
          <p className="ml-4">"vol_eau_min": double,</p>
          <p className="ml-4">"accessibilite": "A" | "B" | "C",</p>
          <p className="ml-4">"disponibilite": "DI" | "ND",</p>
          <p className="ml-4">"derniere_verification": date,</p>
          <p className="ml-4">"nb_raccordement": int</p>
          <p className="ml-4">"num_dep": int</p>
          <p>{"}"}</p>
        </div>
      </div>

      {/* Boutons d'action */}
      <div className="grid grid-cols-2 gap-4">
        {/* BOUTON RESET (Anciennement Importer) */}
        <button 
          onClick={handleReset}
          disabled={loading}
          className={`flex flex-col items-center justify-center p-10 rounded-3xl border-2 border-dashed transition-all group ${
            loading ? 'bg-slate-100 border-slate-200 cursor-not-allowed' : 'bg-white border-red-200 hover:border-red-400 hover:bg-red-50'
          }`}
        >
          <RotateCcw className={`mb-2 ${loading ? 'animate-spin text-slate-400' : 'text-red-400 group-hover:rotate-[-45deg] transition-transform'}`} size={32} />
          <span className="font-bold text-slate-600">
            {loading ? "RÉINITIALISATION..." : "RESET BASE ORIGINE"}
          </span>
          {message && <span className="text-xs text-green-600 mt-2 font-bold animate-bounce">{message}</span>}
        </button>
        
        <button 
          onClick={handleExport}
          className="flex flex-col items-center justify-center p-10 bg-white border-2 border-slate-200 rounded-3xl hover:bg-slate-50 transition group shadow-sm"
        >
          <Download className="mb-2 text-slate-400 group-hover:text-green-500 transition-transform group-hover:translate-y-1" size={32} />
          <span className="font-bold text-slate-600">Exporter Sauvegarde</span>
        </button>
      </div>
    </div>
  );
};

export default DataManager;