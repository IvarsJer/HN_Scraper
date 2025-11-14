import React, { useState, useEffect } from 'react';
import './App.css';
import ArticlesTable from './components/ArticlesTable';
import axios from 'axios';

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalArticles, setTotalArticles] = useState(0);
  const perPage = 10;

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetchArticles(currentPage);
  }, [currentPage]);

  const fetchArticles = async (page) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_URL}/api/articles`, {
        params: {
          page: page,
          per_page: perPage,
          sort_by: 'date_scraped',
          order: 'desc'
        }
      });

      setArticles(response.data.articles);
      setTotalPages(response.data.pages);
      setTotalArticles(response.data.total);
    } catch (err) {
      setError(err.message || 'Failed to fetch articles');
      console.error('Error fetching articles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const handleRefresh = () => {
    fetchArticles(currentPage);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🗞️ Hacker News Scraper</h1>
        <p>Browse and analyze articles from Hacker News</p>
      </header>

      <main className="App-main">
        <div className="controls">
          <button onClick={handleRefresh} className="refresh-btn">
            🔄 Refresh
          </button>
          <div className="stats">
            Total Articles: <strong>{totalArticles}</strong>
          </div>
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading articles...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>❌ Error: {error}</p>
            <button onClick={handleRefresh}>Try Again</button>
          </div>
        )}

        {!loading && !error && (
          <>
            <ArticlesTable articles={articles} />

            {totalPages > 1 && (
              <div className="pagination">
                <button
                  onClick={() => handlePageChange(1)}
                  disabled={currentPage === 1}
                  className="page-btn"
                >
                  ⏮️ First
                </button>

                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="page-btn"
                >
                  ◀️ Previous
                </button>

                <span className="page-info">
                  Page {currentPage} of {totalPages}
                </span>

                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="page-btn"
                >
                  Next ▶️
                </button>

                <button
                  onClick={() => handlePageChange(totalPages)}
                  disabled={currentPage === totalPages}
                  className="page-btn"
                >
                  Last ⏭️
                </button>
              </div>
            )}
          </>
        )}
      </main>

      <footer className="App-footer">
        <p>Built with React, Flask, and PostgreSQL</p>
      </footer>
    </div>
  );
}

export default App;