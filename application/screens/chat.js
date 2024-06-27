import React, { useState, useEffect} from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, FlatList, KeyboardAvoidingView, Platform, Image, StatusBar, Modal, Alert } from 'react-native';
import ChipIcon from '../constants/icon'
import { getFunctions, httpsCallable } from "firebase/functions";
import Timer from 'react-native-timer';

const chip = ChipIcon.chip;


const ChatScreen = ({firebaseApp}) => {
  const functions = getFunctions(firebaseApp);
  const test = httpsCallable(functions, 'test');
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isModalVisible, setModalVisible] = useState(false);
  const [timer, setTimer] = useState(5);

  useEffect(() => {
    if (isModalVisible && timer > 0) {
      Timer.setTimeout(this, 'timer', () => {
        setTimer(timer - 1);
      }, 1000);
    } else if (timer === 0) {
      setModalVisible(false);
      setTimer(5);
    }
    return () => {
      Timer.clearTimeout(this, 'timer');
    };
  }, [timer, isModalVisible]);

  const handleSend = async () => {
    if (inputText.trim().length > 0) {
      const newMessage = {
        id: messages.length.toString(),
        text: inputText,
        user: 'user',
      };
      setMessages([newMessage, ...messages]);

      try {
        // Call the Firebase Cloud Function
        test({messages: messages, inputText: inputText})
          .then((result) => {
          // Create a new message object for the response
            const newBotMessage = {
              id: (messages.length + 1).toString(),
              text: result.data.response, // Assuming the function returns an object with a 'response' field
              user: 'assistant',
            };
            console.log(messages)
            // Add the bot's response to the messages
            setMessages((prevMessages) =>[newBotMessage, ...prevMessages]);
            if (result.data.response.toLowerCase().includes('task')) {
              setModalVisible(true);
            }
          });
      } catch (error) {
        console.error('Error calling Firebase function:', error);
        // Optionally, you can add an error message to the chat
        const errorMessage = {
          id: (messages.length + 1).toString(),
          text: 'Sorry, there was an error processing your request.',
          user: 'assistant',
        };
        setMessages((prevMessages) => [errorMessage, ...prevMessages]);
      }
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
      <Modal
        transparent={true}
        visible={isModalVisible}
        onRequestClose={() => {
          Alert.alert('Modal has been closed.');
          setModalVisible(!isModalVisible);
        }}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalText}>Task Detected</Text>
            <Text style={styles.modalTimer}>Closing in {timer} seconds...</Text>
          </View>
        </View>
      </Modal>
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
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContainer: {
    width: 300,
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalText: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  modalTimer: {
    fontSize: 16,
    marginTop: 10,
  },
});

export default ChatScreen;
