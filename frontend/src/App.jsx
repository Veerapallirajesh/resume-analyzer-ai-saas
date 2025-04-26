import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jobDesc) return alert('Please upload a file and paste a job description.');

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_desc', jobDesc);

    try {
      const res = await fetch('http://localhost:8000/analyze/', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data.result);
    } catch (err) {
      console.error(err);
      alert('Error analyzing resume.');
    }
  };

  return (
    <div className="flex min-h-screen justify-center items-center flex-col gap-4 p-8 text-center">
      <h1 className="text-4xl font-bold text-slate-800">Resume Analyzer</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 items-center">
        <label className="text-lg">
          Upload Resume (.txt, .pdf, .doc, .docx)
          <input
            type="file"
            accept=".txt,.pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            className="block mt-2"
          />
        </label>
        <label className="text-lg">
          Paste Job Description
          <textarea
            rows="5"
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            className="w-96 border border-gray-300 p-2"
          ></textarea>
        </label>
        <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Analyze
        </button>
      </form>
      {result && (
        <div className="mt-4 max-w-xl">
          <h2 className="text-xl font-semibold">Result</h2>
          <pre className="text-left bg-gray-100 p-4 rounded">{result}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
