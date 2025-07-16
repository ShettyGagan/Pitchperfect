import React from 'react';
import { TrendingUp, Award } from 'lucide-react';


export const ScoreCard = ({
  totalScore,
  maxScore,
  interpretation,
  feedbackSummary
}) => {
  const scorePercentage = Math.round((totalScore / maxScore) * 100);

  return (
    <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 rounded-3xl p-10 text-white mb-12 shadow-2xl">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-2xl mr-4">
            <TrendingUp className="w-8 h-8 text-emerald-400" />
          </div>
          <div>
            <h2 className="text-3xl font-bold">Overall Performance</h2>
            <p className="text-slate-300 text-lg">{interpretation}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-6xl font-bold text-emerald-400 mb-2">{scorePercentage}</div>
          <div className="text-slate-300 font-medium">Score: {totalScore}/{maxScore}</div>
        </div>
      </div>
      <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-8">
        <p className="text-lg leading-relaxed text-slate-100 font-medium">
          {feedbackSummary}
        </p>
      </div>
    </div>
  );
};