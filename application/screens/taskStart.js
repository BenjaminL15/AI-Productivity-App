import React, {useState, useEffect } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const TaskStart = () => {
    const navigation = useNavigation();
    const [displayedText, setDisplayedText] = useState('');
    const [showCursor, setShowCursor] = useState(true);
    const exampleTasks = [
        "I want to plan my friend's party",
        "I want to send emails to my co-workers",
        "I need to study for my exam",
        "I want to buy a father's day gift"
    ]
    const [currentTaskIndex, setCurrentTaskIndex] = useState(0);

    useEffect(() => {
      let index = 0;
      setDisplayedText('');
      const typeInterval = setInterval(() => {
        setDisplayedText((prev) => prev + exampleTasks[currentTaskIndex][index]);
        index++;
        if (index === exampleTasks[currentTaskIndex].length) {
          clearInterval(typeInterval);
        }
      }, 50);
  
      const cursorInterval = setInterval(() => {
        setShowCursor((prev) => !prev);
      }, 500);
  
      const changeTaskTimeout = setTimeout(() => {
        setCurrentTaskIndex((prevIndex) => (prevIndex + 1) % exampleTasks.length);
      }, 6000);
  
      return () => {
        clearInterval(typeInterval);
        clearInterval(cursorInterval);
        clearTimeout(changeTaskTimeout);
      };
    }, [currentTaskIndex]);

    const handleArrowPress = () => {
      navigation.navigate('Chat');
    };

    return (
        <View style={styles.container}>
          <View style={styles.menuIcon}>
            <Text style={styles.menuText}>≡</Text>
          </View>
          <View style={styles.taskContainer}>
            <Text style={styles.taskText}>What task do you have in mind?</Text>
          </View>
        <Text style={styles.exampleTask}>
            {displayedText}
            {showCursor && <Text>|</Text>}
        </Text>
          <TouchableOpacity style={styles.arrowContainer} onPress={handleArrowPress}>
            <AntDesign name="down" size={24} color="#FFA6A6" />
          </TouchableOpacity>
        </View>
      );
    };

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1b1b2f',
    justifyContent: 'center',
    alignItems: 'center',
  },
  menuIcon: {
    position: 'absolute',
    top: 40,
    left: 20,
  },
  menuText: {
    color: '#fff',
    fontSize: 24,
  },
  taskContainer: {
    backgroundColor: '#f2c9d1',
    padding: 20,
    borderRadius: 20,
    bottom: 150,
    height: '35%',
    width: '90%',
    alignItems: 'center',
  },
  taskText: {
    color: '#000',
    fontSize: 24,
    top: 130,
  },
  arrowContainer: {
    alignItems: 'center',
    top: 40,
  },
  exampleTask: {
    color: 'white',
    fontSize: '20',
  }
});

export default TaskStart;
