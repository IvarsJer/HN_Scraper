import React, { useEffect, useRef } from 'react';
import $ from 'jquery';
import 'datatables.net-dt';
import './ArticlesTable.css';

function ArticlesTable({ articles }) {
  const tableRef = useRef(null);
  const dataTableRef = useRef(null);

  useEffect(() => {
    if (dataTableRef.current) {
      dataTableRef.current.destroy();
    }

    if (tableRef.current && articles.length > 0) {
      dataTableRef.current = $(tableRef.current).DataTable({
        data: articles,
        columns: [
          {
            title: 'Title',
            data: 'title',
            render: function(data, type, row) {
              if (type === 'display' && row.link) {
                return `<a href="${row.link}" target="_blank" rel="noopener noreferrer" class="article-link">${data}</a>`;
              }
              return data;
            }
          },
          {
            title: 'Points',
            data: 'points',
            className: 'points-cell',
            render: function(data) {
              return `<span class="points-badge">${data}</span>`;
            }
          },
          {
            title: 'Date Created',
            data: 'date_created',
            render: function(data) {
              if (!data) return 'N/A';
              const date = new Date(data);
              return date.toLocaleString();
            }
          },
          {
            title: 'Date Scraped',
            data: 'date_scraped',
            render: function(data) {
              if (!data) return 'N/A';
              const date = new Date(data);
              return date.toLocaleString();
            }
          },
          {
            title: 'HN ID',
            data: 'hn_id',
            className: 'hn-id-cell',
            render: function(data) {
              return `<a href="https://news.ycombinator.com/item?id=${data}" target="_blank" rel="noopener noreferrer" class="hn-link">${data}</a>`;
            }
          }
        ],
        paging: false,
        searching: true,
        ordering: true,
        order: [[2, 'desc']],
        info: false,
        language: {
          search: 'Search articles:',
          zeroRecords: 'No articles found',
          emptyTable: 'No articles available'
        },
        dom: '<"table-top"f>rt',
        drawCallback: function() {
          $(tableRef.current).find('tbody tr').addClass('table-row');
        }
      });
    }

    // Cleanup
    return () => {
      if (dataTableRef.current) {
        dataTableRef.current.destroy();
        dataTableRef.current = null;
      }
    };
  }, [articles]);

  if (articles.length === 0) {
    return (
      <div className="no-articles">
        <p>📭 No articles found. Try running the scraper first!</p>
        <code>flask scrape</code>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table ref={tableRef} className="articles-table" width="100%"></table>
    </div>
  );
}

export default ArticlesTable;
