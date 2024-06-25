import React from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity } from 'react-native';
import llama from '../constants/image'

const welcomeScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.welcome}>Welcome!</Text>
      <Image source={llama.llama} style={styles.profileImage} />
      <Text style={styles.profileName}>Chip</Text>
      <View style={styles.profileContainer}>
        <Text style={styles.profileTagline}>Personal AI assistant to help you chip away tasks!</Text>
        <View style={styles.line}></View>
        <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Get Started!</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2C2F3F',
    alignItems: 'center',
    justifyContent: 'center',
  },
  welcome: {
    fontSize: 40,
    color: 'white',
    marginBottom: 20,
    position: 'absolute',
    top: 110,
    fontWeight: '700',
  },
  profileContainer: {
    alignItems: 'center',
    height: 800,
    width: 600, 
    backgroundColor: '#ECECEC',
    paddingVertical: 60, 
    paddingHorizontal: 10,
    borderRadius: 300, 
    position: 'absolute', 
    bottom: -350, 
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 20,
    position: 'absolute',
    top: 180,
  },
  profileName: {
    fontSize: 40,
    color: 'white',
    bottom: 130,
    fontWeight: '600',
  },
  profileTagline: {
    fontSize: 15,
    color: 'black',
    textAlign: 'center',
    paddingHorizontal: 20,
    bottom: -40,
  },
  line: {
    width: '20%', 
    borderBottomColor: '#212332',
    borderBottomWidth: 3,
    bottom: -60, 
  },
  button: {
    marginTop: 20,
    backgroundColor: '#212332',
    paddingVertical: 10,
    paddingHorizontal: 40,
    borderRadius: 20,
    bottom: -100,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
});

export default welcomeScreen;
