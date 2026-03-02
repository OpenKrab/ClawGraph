import React, { useState, useEffect } from 'react';

interface GraphViewerProps {
  graphHtml?: string;
  onQuery?: (query: string) => void;
  onFeedback?: (feedback: string) => void;
}

const GraphViewer: React.FC<GraphViewerProps> = ({
  graphHtml,
  onQuery,
  onFeedback
}) => {
  const [query, setQuery] = useState('');
  const [feedback, setFeedback] = useState('');

  const handleQuerySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && onQuery) {
      onQuery(query.trim());
    }
  };

  const handleFeedbackSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (feedback.trim() && onFeedback) {
      onFeedback(feedback.trim());
      setFeedback('');
    }
  };

  return (
    <div className="claw-graph-viewer">
      <div className="query-section mb-4">
        <h3 className="text-lg font-semibold mb-2">Query Knowledge Graph</h3>
        <form onSubmit={handleQuerySubmit} className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter natural language query (e.g., 'projects with deadlines this month')"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Query
          </button>
        </form>
      </div>

      <div className="graph-section mb-4">
        <h3 className="text-lg font-semibold mb-2">Knowledge Graph Visualization</h3>
        {graphHtml ? (
          <iframe
            srcDoc={graphHtml}
            className="w-full h-96 border border-gray-300 rounded-md"
            title="Knowledge Graph"
          />
        ) : (
          <div className="w-full h-96 border border-gray-300 rounded-md flex items-center justify-center text-gray-500">
            No graph loaded. Run visualization script first.
          </div>
        )}
      </div>

      <div className="feedback-section">
        <h3 className="text-lg font-semibold mb-2">Provide Feedback for Learning</h3>
        <form onSubmit={handleFeedbackSubmit} className="flex gap-2">
          <input
            type="text"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="e.g., 'This result was helpful' or 'This is not relevant'"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Send Feedback
          </button>
        </form>
      </div>
    </div>
  );
};

export default GraphViewer;
