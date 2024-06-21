import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, FlatList, KeyboardAvoidingView, Platform, Image, StatusBar } from 'react-native';
import ChipIcon from '../constants/icon'

const chip = ChipIcon.chip;

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const handleSend = () => {
    if (inputText.trim().length > 0) {
      const newMessage = {
        id: messages.length.toString(),
        text: inputText,
        user: 'user',
      };
      setMessages([newMessage, ...messages]);
      setInputText('');
    }
  };

  const renderMessage = ({ item }) => (
    <View style={[styles.messageContainer, item.user === 'user' ? styles.userMessage : styles.aiMessage]}>
      <Text style={styles.messageText}>{item.text}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <TouchableOpacity style={styles.menuButton}>
          <Text style={styles.menuText}>≡</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Chip</Text>
        <Image source={ChipIcon.chip} style={styles.chipIcon} />
      </View>
      <FlatList
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        inverted
        contentContainerStyle={{ flexDirection: 'column' }}
      />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 15 : 0}
        style={styles.KeyboardAvoidingView}
      >
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Type Task Here"
            placeholderTextColor="#fff"
            value={inputText}
            onChangeText={setInputText}
          />
          <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
            <Text style={styles.sendButtonText}>Send</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#212332', 
  },

  headerContainer: {
    backgroundColor: '#121421',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2d3d',
    paddingTop: Platform.OS === 'ios' ? 40 : StatusBar.currentHeight + 5,
    height: Platform.OS === 'ios' ? 100 : StatusBar.currentHeight + 50,
  },

  menuButton: {
    padding: 5,
  },

  menuText: {
    color: 'white',
    fontSize: 24,
  },

  headerTitle: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },

  messageContainer: {
    margin: 8,
    padding: 10,
    borderRadius: 10,
  },

  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#FEE2E2', 
  },

  aiMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#FEE2E2', 
  },

  messageText: {
    color: '#000000', 
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#212332',
    borderTopWidth: 1,
    borderTopColor: '#212332',
  },

  input: {
    flex: 3,
    color: '#ffffff', 
    backgroundColor: '#2a2d3d',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    fontSize: 16,
  },

  sendButton: {
    marginLeft: 10,
    backgroundColor: '#00cec9', 
    borderRadius: 15,
    padding: 10,
  },

  sendButtonText: {
    color: '#ffffff', 
  },

  chipIcon: {
    width: 24,
    height: 24,
    resizeMode: 'contain', 
  },
  
});

export default ChatScreen;
