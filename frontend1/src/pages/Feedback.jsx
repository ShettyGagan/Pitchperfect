import React from 'react';
import { Award, MessageSquare, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ScoreCard } from '../components/ScoreCard';
import { EmotionPieChart } from '../components/EmotionPieChart';
import { TimelineChart } from '../components/TimelineChart';
import { VoiceMetrics } from '../components/VoiceMetrics';
import { StrengthsCard } from '../components/StrengthsCard';
import {useSelector} from 'react-redux';
import { clearAnalysisData } from '../store/analysisSlice';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';


// Process scores for bar chart
const processScoresData = (scores) => {
  return Object.entries(scores).map(([key, value]) => ({
    metric: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    score: value ,
    maxScore: 5
  }));
};



export const Feedback = () => {
  
  const analysisData = useSelector((state) => state.analysis.data);

  const navigate=useNavigate();

  const dispatch=useDispatch();
  const handleClearData=()=>{
    dispatch(clearAnalysisData());
    navigate('/');

  }

  if (!analysisData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-slate-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-emerald-500 mx-auto"></div>
          <p className="mt-4 text-lg text-slate-700">Analyzing your presentation...</p>
        </div>
      </div>
    );
  }

  // Destructure data from Redux store
  const {
    facial_expression_response,
    voice_analysis_response,
    content_analysis_response,
    feedback_response,
    strengths,
    weaknesses,
    suggestions
  } = analysisData;

  const scoresData = processScoresData(feedback_response.scores);
  const totalScore = feedback_response.total_score;
  const maxScore = 25; // 5 categories × 5 points each

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200/50 rounded-full mb-6">
            <Award className="w-4 h-4 text-emerald-600 mr-2" />
            <span className="text-sm font-semibold text-emerald-700">Analysis Complete</span>
          </div>
          <h1 className="text-5xl font-bold text-slate-900 mb-6">
            Speech
            <span className="bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent"> Analysis </span>
            Report
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Comprehensive AI-powered analysis of your presentation performance
          </p>
        </div>

        {/* Overall Score Card */}
        <ScoreCard
          totalScore={totalScore}
          maxScore={maxScore}
          interpretation={feedback_response.interpretation}
          feedbackSummary={feedback_response.feedback_summary}
        />

        {/* Transcription Section */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-200/50 p-10 mb-12">
          <div className="flex items-center mb-8">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 w-14 h-14 rounded-2xl flex items-center justify-center mr-4">
              <MessageSquare className="w-7 h-7 text-blue-600" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-slate-900">Speech Transcription</h3>
              <p className="text-slate-600">AI-generated transcript of your presentation</p>
            </div>
          </div>
          <div className="bg-gradient-to-br from-slate-50 to-slate-100/50 rounded-2xl p-8 border border-slate-200/50">
            <p className="text-slate-700 leading-relaxed text-lg font-medium italic">
              "{voice_analysis_response.transcription}"
            </p>
          </div>
        </div>

        {/* Analysis Sections */}
        <VoiceMetrics
          voiceData={voice_analysis_response}
          engagementMetrics={facial_expression_response.engagement_metrics}
        />

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Emotion Distribution */}
          <EmotionPieChart emotionTimeline={facial_expression_response.emotion_timeline} />

          {/* Performance Scores */}
          <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200/50">
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Performance Breakdown</h3>
            <p className="text-slate-600 mb-6">Detailed scoring across key areas</p>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={scoresData} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="metric" 
                  stroke="#64748b" 
                  fontSize={12}
                  angle={-45}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis domain={[0, 5]} stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e2e8f0', 
                    borderRadius: '12px',
                    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)'
                  }} 
                />
                <Bar dataKey="score" fill="#7c3aed" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Emotion Timeline */}
        <TimelineChart emotionTimeline={facial_expression_response.emotion_timeline} />

        {/* Insights Grid */}
        <StrengthsCard
          strengths={strengths}
          weaknesses={weaknesses}
          suggestions={suggestions}
        />

        {/* CTA Section */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-3xl p-12 mt-16 text-center text-white">
          <div className="max-w-3xl mx-auto">
            <div className="bg-white/10 backdrop-blur-sm w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Zap className="w-8 h-8 text-emerald-400" />
            </div>
            <h2 className="text-3xl font-bold mb-4">Continue Improving</h2>
            <p className="text-xl text-slate-300 mb-8">
              Practice makes perfect. Upload another presentation to track your progress
            </p>
            <button onClick={handleClearData} className="bg-white text-slate-900 px-8 py-4 rounded-xl font-semibold hover:bg-slate-100 transition-colors shadow-lg text-lg">
              Analyze Another Presentation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};