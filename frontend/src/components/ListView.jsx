import React, { useEffect, useState } from 'react';
import ListItem from './ListItem';

export default function ListView() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await fetch('https://700-digital-equity-production-c1d4.up.railway.app/api/leaderboard'); // Replace with your API endpoint
        const data = await response.json();
        console.log('Fetched leaderboard data:', data); // Debugging line
        setRecords(data);
      } catch (error) {
        console.error('Error fetching leaderboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return <p>Loading leaderboard...</p>;
  }

  return (
    <div className="list-view">
      <div className="list-view-header">
        <span>Name</span>
        <span>Region</span>
        <span>Latency</span>
        <span>Upload Speed</span>
        <span>Download Speed</span>
        <span>Device</span>
        <span>Date</span>
        <span>Location</span>
      </div>
      <ul className="list-view-items">
        {records.map((record, index) => (
          <ListItem key={index} record={record} />
        ))}
      </ul>
    </div>
  );
};
