import { useEffect, useState } from 'react';
import axios from 'axios';

type Persona = {
  id: number;
  name: string;
  description: string;
  prompt: string;
};

function App() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [form, setForm] = useState({ name: '', description: '', prompt: '' });
  const [editingId, setEditingId] = useState<number | null>(null);
  const API_BASE = import.meta.env.VITE_API_BASE;
  
  const fetchPersonas = async () => {
    console.log('API_BASE =', API_BASE);
    const res = await axios.get(`${API_BASE}/personas`);
    console.log(res.data);
    setPersonas(res.data);
  };

  useEffect(() => {
    fetchPersonas();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (editingId !== null) {
      await axios.put(`${API_BASE}/personas/${editingId}`, form);
    } else {
      await axios.post(`${API_BASE}/personas`, form);
    }

    setForm({ name: '', description: '', prompt: '' });
    setEditingId(null);
    fetchPersonas();
  };

  const handleEdit = (persona: Persona) => {
    setForm({
      name: persona.name,
      description: persona.description,
      prompt: persona.prompt,
    });
    setEditingId(persona.id);
  };

  const handleDelete = async (id: number) => {
    await axios.delete(`${API_BASE}/personas/${id}`);
    fetchPersonas();
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Personas</h1>

      <form onSubmit={handleSubmit} className="space-y-2 mb-6">
        <input
          className="w-full p-2 border rounded"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          className="w-full p-2 border rounded"
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <textarea
          className="w-full p-2 border rounded"
          placeholder="Prompt"
          value={form.prompt}
          onChange={(e) => setForm({ ...form, prompt: e.target.value })}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          type="submit"
        >
          {editingId ? 'Update Persona' : 'Create Persona'}
        </button>
      </form>

      <ul className="space-y-4">
        {personas.map((p) => (
          <li key={p.id} className="border p-4 rounded shadow-sm">
            <div className="font-semibold text-lg">{p.name}</div>
            <div className="italic text-sm">{p.description}</div>
            <div className="text-xs mt-1 text-gray-600" style={{ whiteSpace: 'pre-wrap' }}>
                {p.prompt}
            </div>
            <div className="mt-2 space-x-2">
              <button
                onClick={() => handleEdit(p)}
                className="text-blue-500 hover:underline"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(p.id)}
                className="text-red-500 hover:underline"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
