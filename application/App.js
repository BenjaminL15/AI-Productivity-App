// App.js
import React from 'react';
import { StyleSheet, View } from 'react-native';
import ChatScreen from '../application/screens/chat'; 

const App = () => {
  return (
    <View style={styles.container}>
      <ChatScreen />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;
