import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

// Removed TypeScript interfaces since this is a JavaScript file.

export const EmotionPieChart = ({ emotionTimeline }) => {
  const processEmotionData = (timeline) => {
    const emotionCounts = timeline.reduce((acc, item) => {
      acc[item.emotion] = (acc[item.emotion] || 0) + 1;
      return acc;
    }, {});

    const colors = {
      happy: '#10b981',
      sad: '#f59e0b',
      fear: '#ef4444',
      neutral: '#6b7280',
      angry: '#dc2626',
      surprised: '#8b5cf6'
    };

    return Object.entries(emotionCounts).map(([emotion, count]) => ({
      name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
      value: count ,
      color: colors[emotion] || '#6b7280'
    }));
  };

  const emotionData = processEmotionData(emotionTimeline);

  return (
    <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50">
      <h3 className="text-2xl font-bold text-slate-900 mb-2">Emotion Distribution</h3>
      <p className="text-slate-600 mb-6">Facial expression analysis throughout presentation</p>
      <ResponsiveContainer width="100%" height={320}>
        <PieChart>
          <Pie
            data={emotionData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            strokeWidth={2}
            stroke="#fff"
          >
            {emotionData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #e2e8f0', 
              borderRadius: '12px',
              boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)'
            }} 
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};