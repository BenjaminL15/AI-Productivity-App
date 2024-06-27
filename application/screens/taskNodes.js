import React, { useEffect, useState} from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const TaskNode = () => {
    const [firstUserMessage, setFirstUserMessage] = useState('');
  
    useEffect(() => {
      async function getStoredMessage() {
        try {
          const storedMessage = await AsyncStorage.getItem('firstUserMessage');
          if (storedMessage !== null) {
            setFirstUserMessage(storedMessage);
          }
        } catch (error) {
          console.error('Error retrieving stored message:', error);
        }
      }
  
      getStoredMessage();
    }, []);
  
    return (
      <View style={styles.container}>
        <Text style={styles.messageText}>First User Message:</Text>
        <Text style={styles.messageText}>{firstUserMessage}</Text>
      </View>
    );
  };

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#1a1a2e',
      padding: 20,
      borderRadius: 10,
      marginBottom: 10,
    },
    messageText: {
      fontSize: 16,
      color: '#ffffff',
      marginBottom: 5,
    },
  });

export default TaskNode;
