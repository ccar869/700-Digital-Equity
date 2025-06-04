import React from 'react';

export default function ListItem({ record }){
  return (
    <li className="list-item">
      <div className="list-item-content">
      <span>{record.name}</span>
        <span>{record.region}</span>
        <span>{record.avg_ping} ms</span>
        <span>{record.upload} MB/s</span>
        <span>{record.download} MB/s</span>
        <span>{record.device}</span>
        <span>{record.timestamp ? new Date(record.timestamp).toLocaleString() : ''}</span>
        <span>
          {record.location
            ? `${record.location.latitude}, ${record.location.longitude}`
            : ''}
        </span>
      </div>
    </li>
  );
};
