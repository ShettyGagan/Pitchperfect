import React from 'react';
import { CheckCircle, Target, Lightbulb } from 'lucide-react';


export const StrengthsCard = ({ strengths, weaknesses, suggestions }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-8 border border-emerald-200/50">
        <div className="flex items-center mb-6">
          <div className="bg-white w-14 h-14 rounded-2xl flex items-center justify-center mr-4 shadow-sm">
            <CheckCircle className="w-7 h-7 text-emerald-600" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-slate-900">Strengths</h3>
            <p className="text-emerald-700 font-medium">What you did well</p>
          </div>
        </div>
        <ul className="space-y-4">
          {strengths.map((strength, index) => (
            <li key={index} className="flex items-start">
              <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
              <span className="text-slate-700 font-medium leading-relaxed capitalize">{strength}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-8 border border-amber-200/50">
        <div className="flex items-center mb-6">
          <div className="bg-white w-14 h-14 rounded-2xl flex items-center justify-center mr-4 shadow-sm">
            <Target className="w-7 h-7 text-amber-600" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-slate-900">Areas to Improve</h3>
            <p className="text-amber-700 font-medium">Focus areas</p>
          </div>
        </div>
        <ul className="space-y-4">
          {weaknesses.map((weakness, index) => (
            <li key={index} className="flex items-start">
              <div className="w-2 h-2 bg-amber-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
              <span className="text-slate-700 font-medium leading-relaxed capitalize">{weakness}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-2xl p-8 border border-violet-200/50">
        <div className="flex items-center mb-6">
          <div className="bg-white w-14 h-14 rounded-2xl flex items-center justify-center mr-4 shadow-sm">
            <Lightbulb className="w-7 h-7 text-violet-600" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-slate-900">Recommendations</h3>
            <p className="text-violet-700 font-medium">Action items</p>
          </div>
        </div>
        <ul className="space-y-4">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="flex items-start">
              <div className="w-2 h-2 bg-violet-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
              <span className="text-slate-700 font-medium leading-relaxed capitalize">{suggestion}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};