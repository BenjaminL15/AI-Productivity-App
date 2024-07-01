// App.js
import React from 'react';
import { StyleSheet, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator, CardStyleInterpolators } from '@react-navigation/stack';
import ChatScreen from '../application/screens/chat'; 
import WelcomeScreen from '../application/screens/welcome';
import TaskStart from '../application/screens/taskStart';

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

const Stack = createStackNavigator();

const verticalSwipeTransition = {
  gestureDirection: 'vertical',
  transitionSpec: {
    open: {
      animation: 'timing',
      config: {
        duration: 300,
      },
    },
    close: {
      animation: 'timing',
      config: {
        duration: 300,
      },
    },
  },
  cardStyleInterpolator: CardStyleInterpolators.forVerticalIOS,
};

const fadeTransition = {
  gestureDirection: 'horizontal',
  transitionSpec: {
    open: {
      animation: 'timing',
      config: {
        duration: 300,
      },
    },
    close: {
      animation: 'timing',
      config: {
        duration: 300,
      },
    },
  },
  cardStyleInterpolator: ({ current }) => ({
    cardStyle: {
      opacity: current.progress,
    },
  }),
};

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Welcome" component={WelcomeScreen} options={{headerShown: false}}/>
        <Stack.Screen name="TaskStart" component={TaskStart} options={{headerShown: false, ...fadeTransition}} />
        <Stack.Screen 
          name="Chat" 
          component={ChatScreen} 
          initialParams={{ firebaseApp: app }} 
          options={{ 
            ...verticalSwipeTransition,
            headerShown: false 
          }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;
