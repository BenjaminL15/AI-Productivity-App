// App.js
import React from 'react';
import { StyleSheet, View } from 'react-native';
import ChatScreen from '../application/screens/chat'; 

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFunctions, httpsCallable } from "firebase/functions";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBZYC-AjZHJXODHAkxL2ylSsVYUAubuXdg",
  authDomain: "project-f6f0e.firebaseapp.com",
  projectId: "project-f6f0e",
  storageBucket: "project-f6f0e.appspot.com",
  messagingSenderId: "843684034294",
  appId: "1:843684034294:web:8f98b26a438092d98d1ed7",
  measurementId: "G-L55B3S8QY1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const functions = getFunctions(app);
const analytics = getAnalytics(app);

const App = () => {
  return (
    <View style={styles.container}>
      <ChatScreen firebaseApp={app}/>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;
