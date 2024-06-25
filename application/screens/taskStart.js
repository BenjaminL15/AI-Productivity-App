import React from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';

const taskStart = () => {
  return (
    <View style={styles.container}>
      <View style={styles.menuIcon}>
        <Text style={styles.menuText}>≡</Text>
      </View>
      <View style={styles.taskContainer}>
        <Text style={styles.taskText}>What task do you have in mind?</Text>
      </View>
      <TextInput
        style={styles.input}
        placeholder="I want to plan my friend's party"
        placeholderTextColor="#fff"
      />
      <TouchableOpacity style={styles.arrowContainer}>
        <Text style={styles.arrow}>▼</Text>
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
    borderRadius: 10,
    marginBottom: 20,
  },
  taskText: {
    color: '#000',
    fontSize: 24,
    textAlign: 'center',
  },
  input: {
    width: '80%',
    padding: 10,
    borderColor: '#fff',
    borderWidth: 1,
    borderRadius: 5,
    color: '#fff',
    fontSize: 18,
    marginBottom: 20,
  },
  arrowContainer: {
    alignItems: 'center',
  },
  arrow: {
    color: '#f2c9d1',
    fontSize: 24,
  },
});

export default taskStart;
