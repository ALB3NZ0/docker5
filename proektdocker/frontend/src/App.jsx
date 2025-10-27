import { useState, useEffect } from 'react';

function App() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [description, setDescription] = useState('');

  const API_URL = "http://localhost:5555/books";

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setBooks(data))
      .catch(err => console.error(err));
  }, []);

  const handleAdd = async () => {
    const newBook = { title, author, description };
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newBook)
      });
      const data = await res.json();
      setBooks([...books, data]);
      
      setTitle(""); setAuthor(""); setDescription("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Библиотека книг</h1>
      <ul>
        {books.map(book => (
          <li key={book.id}>
            Название: {book.title} <br />
            Автор: {book.author} <br />
            Описание: {book.description} <br />
          </li>
        ))}
      </ul>

      <h2>Добавить книгу</h2>
      <input placeholder="Название" value={title} onChange={e => setTitle(e.target.value)} />
      <input placeholder="Автор" value={author} onChange={e => setAuthor(e.target.value)} />
      <input placeholder="Описание" value={description} onChange={e => setDescription(e.target.value)} />
      <button onClick={handleAdd}>Добавить</button>
    </div>
  );
}

export default App;
