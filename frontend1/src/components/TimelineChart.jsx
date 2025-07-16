import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';



export const TimelineChart = ({ emotionTimeline }) => {
  const processEmotionTimeline = (timeline) => {
    return timeline.map(item => ({
      timestamp: parseFloat(item.timestamp.toFixed(1)),
      emotion: item.emotion,
      // Convert emotions to numeric values for visualization
      value: item.emotion === 'happy' ? 5 : 
             item.emotion === 'neutral' ? 3 : 
             item.emotion === 'sad' ? 2 : 
             item.emotion === 'fear' ? 1 : 3
    }));
  };

  const timelineData = processEmotionTimeline(emotionTimeline);

  return (
    <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50 mb-12">
      <h3 className="text-2xl font-bold text-slate-900 mb-2">Emotion Timeline</h3>
      <p className="text-slate-600 mb-6">Emotional state changes throughout your presentation</p>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={timelineData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis 
            dataKey="timestamp" 
            stroke="#64748b"
            label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            domain={[0, 6]} 
            stroke="#64748b"
            tickFormatter={(value) => {
              const emotions = ['', 'Fear', 'Sad', 'Neutral', '', 'Happy'];
              return emotions[value] || '';
            }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #e2e8f0', 
              borderRadius: '12px',
              boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)'
            }}
            labelFormatter={(value) => `Time: ${value}s`}
            formatter={(value, name, props) => [props.payload.emotion, 'Emotion']}
          />
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke="#7c3aed" 
            strokeWidth={3}
            dot={{ fill: '#7c3aed', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: '#7c3aed', strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};