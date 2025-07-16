import React from 'react';
import { Mic2, Eye, Smile, Volume2 } from 'lucide-react';


export const VoiceMetrics= ({ voiceData, engagementMetrics }) => {
  const processVoiceMetrics = (voiceData) => {
    return [
      { 
        metric: 'Speech Rate', 
        value: parseFloat(voiceData.speech_rate_wpm), 
        unit: 'WPM',
        optimal: '120-160',
        status: parseFloat(voiceData.speech_rate_wpm) < 120 ? 'low' : 'good'
      },
      { 
        metric: 'Pitch Variation', 
        value: parseFloat(voiceData.pitch_variation), 
        unit: 'Hz',
        optimal: '50-200',
        status: parseFloat(voiceData.pitch_variation) > 200 ? 'high' : 'good'
      },
      { 
        metric: 'Volume Consistency', 
        value: (parseFloat(voiceData.volume_consistency) * 100).toFixed(2), 
        unit: '%',
        optimal: '<5%',
        status: parseFloat(voiceData.volume_consistency) < 0.05 ? 'good' : 'needs improvement'
      }
    ];
  };

  const voiceMetrics = processVoiceMetrics(voiceData);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
      {/* Facial Expression Analysis */}
      <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50 hover:shadow-lg transition-all duration-300">
        <div className="flex items-center mb-6">
          <div className="bg-gradient-to-br from-emerald-50 to-teal-50 w-14 h-14 rounded-2xl flex items-center justify-center mr-4">
            <Eye className="w-7 h-7 text-emerald-600" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-slate-900">Facial Expression</h3>
            <p className="text-slate-500 text-sm">Emotion & Engagement Analysis</p>
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
            <div className="flex items-center">
              <Eye className="w-5 h-5 text-blue-600 mr-2" />
              <span className="font-medium">Eye Contact</span>
            </div>
            <span className="font-bold text-blue-600">
              {(engagementMetrics.eye_contact_frequency * 100).toFixed(0)}%
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
            <div className="flex items-center">
              <Smile className="w-5 h-5 text-emerald-600 mr-2" />
              <span className="font-medium">Smile Frequency</span>
            </div>
            <span className="font-bold text-emerald-600">
              {(engagementMetrics.smile_frequency * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* Voice Analysis */}
      <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50 hover:shadow-lg transition-all duration-300">
        <div className="flex items-center mb-6">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 w-14 h-14 rounded-2xl flex items-center justify-center mr-4">
            <Mic2 className="w-7 h-7 text-blue-600" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-slate-900">Voice Analysis</h3>
            <p className="text-slate-500 text-sm">Speech Quality Metrics</p>
          </div>
        </div>
        <div className="space-y-3">
          {voiceMetrics.map((metric, index) => (
            <div key={index} className="p-3 bg-slate-50 rounded-lg">
              <div className="flex justify-between items-center mb-1">
                <span className="font-medium text-sm">{metric.metric}</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  metric.status === 'good' ? 'bg-emerald-100 text-emerald-700' : 
                  metric.status === 'low' ? 'bg-amber-100 text-amber-700' : 
                  'bg-red-100 text-red-700'
                }`}>
                  {metric.status}
                </span>
              </div>
              <div className="text-lg font-bold text-slate-900">
                {metric.value} {metric.unit}
              </div>
              <div className="text-xs text-slate-500">
                Optimal: {metric.optimal}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Content Analysis */}
      <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50 hover:shadow-lg transition-all duration-300">
        <div className="flex items-center mb-6">
          <div className="bg-gradient-to-br from-violet-50 to-purple-50 w-14 h-14 rounded-2xl flex items-center justify-center mr-4">
            <Volume2 className="w-7 h-7 text-violet-600" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-slate-900">Content Quality</h3>
            <p className="text-slate-500 text-sm">Structure & Clarity</p>
          </div>
        </div>
        <div className="space-y-4">
          <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200">
            <div className="flex items-center mb-2">
              <div className="w-2 h-2 bg-emerald-500 rounded-full mr-2"></div>
              <span className="font-medium text-emerald-800">Grammar</span>
            </div>
            <p className="text-sm text-emerald-700">
              No grammar issues detected
            </p>
          </div>
          <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center mb-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
              <span className="font-medium text-blue-800">Filler Words</span>
            </div>
            <p className="text-sm text-blue-700">
              Minimal filler words detected
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};