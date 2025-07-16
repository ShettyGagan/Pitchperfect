import React, { useState } from 'react';
import { Upload, FileVideo, Bot, Info, FileText, Zap, Shield, TrendingUp, Clock } from 'lucide-react';
import axios from "axios"
import {useDispatch} from 'react-redux';
import {setAnalysisData} from '../store/analysisSlice';
import { useNavigate } from 'react-router-dom';

export const Home = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedFile(file);
    } else {
      alert('Please select a valid video file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    
    // Simulate API call
  try{

    const formdata=new FormData();
    formdata.append("file",selectedFile)

    const upload= await axios.post("http://localhost:1010/upload",formdata,{
      headers:{
        "Content-Type": "multipart/form-data",
      }
    });

    const video_path=upload.data.file_path;

    //analysing video
    const analysisResponse=await axios.post("http://localhost:1010/analyze",{
      video_url:video_path,
    });

    const analysisreport=analysisResponse.data;

    

  dispatch(setAnalysisData(analysisreport));

  if(
    analysisreport &&
    analysisreport.voice_analysis_response &&
    analysisreport.voice_analysis_response.transcription
    ){
    setTranscription(JSON.stringify(analysisreport.voice_analysis_response.transcription,null,2));
    }
  else {
  console.warn("Transcription missing in analysis response", analysisreport);
}

  }catch (error) {
    console.error("Upload or analysis error:", error);
    alert("Something went wrong: " + (error.response?.data?.error || error.message));
  } finally {
    setIsUploading(false);
  }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-violet-50 to-indigo-50 border border-violet-200/50 rounded-full mb-6">
            <Zap className="w-4 h-4 text-violet-600 mr-2" />
            <span className="text-sm font-semibold text-violet-700">AI-Powered Speech Analysis</span>
          </div>
          <h1 className="text-5xl font-bold text-slate-900 mb-6 leading-tight">
            Master Your
            <span className="bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent"> Presentation </span>
            Skills
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Transform your speaking abilities with enterprise-grade AI analysis. Get actionable insights 
            on delivery, engagement, and impact to become a more confident presenter.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="group bg-white rounded-2xl p-8 shadow-sm border border-slate-200/50 hover:shadow-xl hover:shadow-slate-900/5 transition-all duration-300">
            <div className="bg-gradient-to-br from-emerald-50 to-teal-50 w-14 h-14 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <Bot className="w-7 h-7 text-emerald-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-3">Advanced AI Engine</h3>
            <p className="text-slate-600 leading-relaxed">
              Cutting-edge computer vision and NLP technology analyzes facial expressions, 
              voice patterns, and content structure with 95% accuracy.
            </p>
          </div>

          <div className="group bg-white rounded-2xl p-8 shadow-sm border border-slate-200/50 hover:shadow-xl hover:shadow-slate-900/5 transition-all duration-300">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 w-14 h-14 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <TrendingUp className="w-7 h-7 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-3">Actionable Insights</h3>
            <p className="text-slate-600 leading-relaxed">
              Receive detailed feedback with specific recommendations to improve your 
              speaking confidence, clarity, and audience engagement.
            </p>
          </div>

          <div className="group bg-white rounded-2xl p-8 shadow-sm border border-slate-200/50 hover:shadow-xl hover:shadow-slate-900/5 transition-all duration-300">
            <div className="bg-gradient-to-br from-violet-50 to-purple-50 w-14 h-14 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <Shield className="w-7 h-7 text-violet-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-3">Enterprise Security</h3>
            <p className="text-slate-600 leading-relaxed">
              Your presentations are processed with bank-level encryption and 
              automatically deleted after analysis for complete privacy protection.
            </p>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-200/50 p-10 mb-12">
          <div className="flex items-center justify-center mb-8">
            <div className="bg-gradient-to-br from-slate-100 to-slate-200 w-16 h-16 rounded-2xl flex items-center justify-center mr-4">
              <FileVideo className="w-8 h-8 text-slate-700" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-slate-900">Upload Your Presentation</h2>
              <p className="text-slate-600 mt-1">Get professional analysis in under 2 minutes</p>
            </div>
          </div>
          
          <div className="space-y-8">
            <div className="relative border-2 border-dashed border-slate-300 rounded-2xl p-16 text-center hover:border-violet-400 hover:bg-gradient-to-br hover:from-violet-50/50 hover:to-indigo-50/50 transition-all duration-300 group">
              <input
                type="file"
                accept="video/*"
                onChange={handleFileSelect}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="video-upload"
              />
              <div className="group-hover:scale-105 transition-transform duration-300">
                <div className="bg-gradient-to-br from-slate-100 to-slate-200 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:from-violet-100 group-hover:to-indigo-100 transition-all duration-300">
                  <Upload className="w-10 h-10 text-slate-600 group-hover:text-violet-600 transition-colors duration-300" />
                </div>
                <h3 className="text-2xl font-semibold text-slate-900 mb-3">
                  Drop your video here or click to browse
                </h3>
                <p className="text-slate-500 text-lg">
                  Supports MP4, MOV, AVI • Maximum 100MB • 2-15 minutes optimal
                </p>
              </div>
            </div>



            {selectedFile && (
              <div className="bg-gradient-to-r from-violet-50 to-indigo-50 border border-violet-200/50 rounded-2xl p-8">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="bg-white w-12 h-12 rounded-xl flex items-center justify-center mr-4 shadow-sm">
                      <FileVideo className="w-6 h-6 text-violet-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-900 text-lg">
                        {selectedFile.name}
                      </h4>
                      <p className="text-violet-600 font-medium">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • Ready for analysis
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={handleUpload}
                    disabled={isUploading}
                    className="bg-gradient-to-r from-slate-900 to-slate-800 text-white px-8 py-3 rounded-xl font-semibold hover:from-slate-800 hover:to-slate-700 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-slate-900/25 flex items-center space-x-2"
                  >
                    {isUploading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Zap className="w-5 h-5" />
                        <span>Start Analysis</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-12 mb-12 text-white">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">How It Works</h2>
            <p className="text-slate-300 text-lg max-w-2xl mx-auto">
              Our AI analyzes multiple dimensions of your presentation to provide comprehensive feedback
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <FileVideo className="w-8 h-8 text-emerald-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">1. Upload & Process</h3>
              <p className="text-slate-300">
                Secure upload with automatic transcription and video analysis initialization
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Bot className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">2. AI Analysis</h3>
              <p className="text-slate-300">
                Multi-modal AI examines facial expressions, voice patterns, and content structure
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <TrendingUp className="w-8 h-8 text-violet-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">3. Get Insights</h3>
              <p className="text-slate-300">
                Receive detailed feedback with actionable recommendations for improvement
              </p>
            </div>
          </div>
        </div>

        {/* Transcription Display */}
        {transcription && (
          <div className="bg-white rounded-3xl shadow-sm border border-slate-200/50 p-10">
            <div className="flex items-center mb-8">
              <div className="bg-gradient-to-br from-emerald-50 to-teal-50 w-16 h-16 rounded-2xl flex items-center justify-center mr-4">
                <FileText className="w-8 h-8 text-emerald-600" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-slate-900">Speech Transcription</h2>
                <p className="text-slate-600 mt-1">AI-generated transcript with 98% accuracy</p>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-slate-50 to-slate-100/50 rounded-2xl p-8 border border-slate-200/50 mb-8">
              <p className="text-slate-700 leading-relaxed text-lg font-medium">
                "{transcription}"
              </p>
            </div>
            
            <div className="text-center">
              <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200/50 rounded-full mb-6">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mr-3 animate-pulse"></div>
                <span className="font-semibold text-emerald-800">Analysis Complete</span>
                <Clock className="w-4 h-4 text-emerald-600 ml-2" />
              </div>
              <p className="text-slate-600 mb-8 text-lg">
                Your presentation has been successfully analyzed with enterprise-grade AI. 
                View comprehensive insights and personalized recommendations.
              </p>
              <a
                onClick={()=>navigate('/feedback')}
                className="inline-flex items-center px-10 py-4 bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-xl font-semibold hover:from-slate-800 hover:to-slate-700 transition-all duration-200 shadow-lg shadow-slate-900/25 text-lg"
              >
                <TrendingUp className="w-5 h-5 mr-2" />
                View Analytics Dashboard
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};