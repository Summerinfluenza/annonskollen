import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Search, Loader2, CheckCircle2, Briefcase } from 'lucide-react';

// Define the API Base URL
const API_BASE = 'http://localhost:3000/api';

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [userId] = useState("user_" + Math.floor(Math.random() * 1000)); // Unique ID for testing
  const [step, setStep] = useState<'upload' | 'matching' | 'done'>('upload');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  // 1. Upload and Extract PDF
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      await axios.post(`${API_BASE}/resume/upload`, formData);
      setStep('matching');
    } catch (err) {
      alert("Extraction failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  // 2. Trigger Job Match
  const handleMatch = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/jobs/match`, { 
        user_id: userId,
        municipality: "Stockholm" 
      });
      setResults(response.data);
      setStep('done');
    } catch (err) {
      alert("Matching failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 flex justify-center">
      <div className="max-w-xl w-full space-y-6">
        <header className="text-center mb-10">
          <h1 className="text-3xl font-bold text-slate-900">Annonskollen AI</h1>
          <p className="text-slate-500 mt-2">Current Session: {userId}</p>
        </header>

        {/* Step 1: Upload */}
        <div className={`bg-white p-8 rounded-2xl border shadow-sm transition-all ${step !== 'upload' ? 'opacity-50 pointer-events-none scale-95' : ''}`}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">1</div>
            <h2 className="text-xl font-semibold">Upload Resume</h2>
          </div>
          
          <input 
            type="file" 
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="mt-6 w-full bg-blue-600 text-white py-3 rounded-xl font-medium hover:bg-blue-700 flex justify-center items-center gap-2"
          >
            {loading && step === 'upload' ? <Loader2 className="animate-spin" /> : <Upload size={18}/>}
            Analyze Resume
          </button>
        </div>

        {/* Step 2: Match */}
        <div className={`bg-white p-8 rounded-2xl border shadow-sm transition-all ${step !== 'matching' ? 'opacity-50 pointer-events-none scale-95' : ''}`}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">2</div>
            <h2 className="text-xl font-semibold">Match with Jobs</h2>
          </div>
          
          <button
            onClick={handleMatch}
            disabled={loading}
            className="w-full bg-slate-900 text-white py-3 rounded-xl font-medium hover:bg-slate-800 flex justify-center items-center gap-2"
          >
            {loading && step === 'matching' ? <Loader2 className="animate-spin" /> : <Search size={18}/>}
            Find My Matches
          </button>
        </div>

        {/* Step 3: Success */}
        {step === 'done' && (
          <div className="bg-green-50 border border-green-200 p-6 rounded-2xl text-center animate-in fade-in zoom-in duration-300">
            <CheckCircle2 className="text-green-600 mx-auto mb-3" size={48} />
            <h3 className="text-green-800 font-bold text-lg">Process Complete!</h3>
            <p className="text-green-700 mt-1">Python is now processing your tags in the background.</p>
            <pre className="mt-4 text-xs bg-white p-3 rounded border text-left overflow-auto max-h-40">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}