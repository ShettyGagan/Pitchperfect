import {combineReducers, configureStore} from '@reduxjs/toolkit';
import analysisReducer from './analysisSlice';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER
} from 'redux-persist';

import storage from 'redux-persist/lib/storage';
import { version } from 'react';

const persistConfig={
  key:'root',
  version:1,
  storage,
  whitelist: ['analysis'],

}

const rootReducer=combineReducers({
  analysis:analysisReducer,
});

const persistedReducer=persistReducer(persistConfig,rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(store);
