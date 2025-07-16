import {createSlice} from '@reduxjs/toolkit'
import { data } from 'react-router-dom'

// const persistedState = (() => {
//   try {
//     const serializedState = localStorage.getItem('analysisData');
//     if (serializedState === null) return { data: null };
//     return { data: JSON.parse(serializedState) };
//   } catch (e) {
//     return { data: null };
//   }
// })();


const analysisSlice = createSlice({
    name:'analysis',
    initialState:{data:null},
    reducers:{
        setAnalysisData(state,action){
            state.data=action.payload;
        },
        clearAnalysisData(state){
            state.data=null;
        }
    },
});

export const{setAnalysisData,clearAnalysisData} = analysisSlice.actions;
export default analysisSlice.reducer;