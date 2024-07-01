import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, FlatList, KeyboardAvoidingView, Platform, Image, StatusBar, Modal, Alert } from 'react-native';
import ChipIcon from '../constants/icon';
import { getFunctions, httpsCallable } from "firebase/functions";
import Timer from 'react-native-timer';
import { Picker } from '@react-native-picker/picker';

const chip = ChipIcon.chip;

const ChatScreen = ({ firebaseApp }) => {
  const functions = getFunctions(firebaseApp);
  const test = httpsCallable(functions, 'test');
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isTaskModalVisible, setTaskModalVisible] = useState(false);
  const [isTimerModalVisible, setTimerModalVisible] = useState(false);
  const [timer, setTimer] = useState(300);
  const [taskTime, setTaskTime] = useState('');
  const [selectedMinutes, setSelectedMinutes] = useState('0');
  const [selectedSeconds, setSelectedSeconds] = useState('5');
  const [showPicker, setShowPicker] = useState(false);

  const AVAILABLE_MINUTES = Array.from({ length: 60 }, (_, i) => String(i));
  const AVAILABLE_SECONDS = Array.from({ length: 60 }, (_, i) => String(i));

  useEffect(() => {
    if (isTimerModalVisible && timer > 0) {
      Timer.setTimeout(this, 'timer', () => {
        setTimer(timer - 1);
      }, 1000);
    } else if (timer === 0) {
      setTimerModalVisible(false);
      setTimer(5);
    }
    return () => {
      Timer.clearTimeout(this, 'timer');
    };
  }, [timer, isTimerModalVisible]);

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
        test({ messages: messages, inputText: inputText })
          .then((result) => {
            // Create a new message object for the response
            const newBotMessage = {
              id: (messages.length + 1).toString(),
              text: result.data.response, // Assuming the function returns an object with a 'response' field
              user: 'assistant',
            };
            console.log(messages);
            // Add the bot's response to the messages
            setMessages((prevMessages) => [newBotMessage, ...prevMessages]);
            if (result.data.response.toLowerCase().includes('task')) {
              setTaskTime('5:00');
              setTaskModalVisible(true);
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

  const handleYes = () => {
    setTaskModalVisible(false);
    setTimerModalVisible(true);
  };

  const handleNo = () => {
    setTaskModalVisible(false);
    Alert.alert('Task declined.');
  };

  const handleMoreTime = () => {
    setShowPicker(true);
  };

  const handlePickerCancel = () => {
    setShowPicker(false);
  };

  const handlePickerConfirm = () => {
    setTaskModalVisible(false);
    setShowPicker(false);

    const totalSeconds = parseInt(selectedMinutes) * 60 + parseInt(selectedSeconds);

    setTimerModalVisible(true);
    setTimer(totalSeconds);
  };

  const renderMessage = ({ item }) => (
    <View style={[styles.messageContainer, item.user === 'user' ? styles.userMessage : styles.aiMessage]}>
      <Text style={styles.messageText}>{item.text}</Text>
    </View>
  );

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <TouchableOpacity style={styles.menuButton}>
          <Text style={styles.menuText}>≡</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Chip</Text>
        <Image source={chip} style={styles.chipIcon} />
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
        visible={isTaskModalVisible}
        onRequestClose={() => {
          Alert.alert('Modal has been closed.');
          setTaskModalVisible(!isTaskModalVisible);
        }}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.taskModalContainer}>
            <Text style={styles.taskText}>Task Placeholder. Does the amount of time seem reasonable for completion?</Text>
            <View style={styles.timerContainer}>
              <Text style={styles.timerText}>{taskTime}</Text>
            </View>
            <View style={styles.buttonRow}>
              <TouchableOpacity onPress={handleMoreTime} style={[styles.modalButton, styles.moreTimeButton]}>
                <Text style={styles.buttonText}>More time?</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={handleYes} style={[styles.modalButton, styles.yesButton]}>
                <Text style={styles.buttonText}>Yes!</Text>
              </TouchableOpacity>
            </View>
            {showPicker && (
              <View>
                <View style={styles.pickerContainer}>
                  <View style={styles.pickerWrapper}>
                    <Picker
                      style={styles.picker}
                      selectedValue={selectedMinutes}
                      onValueChange={(itemValue) => setSelectedMinutes(itemValue)}
                    >
                      {AVAILABLE_MINUTES.map((value) => (
                        <Picker.Item key={value} label={value} value={value} />
                      ))}
                    </Picker>
                    <Text style={styles.pickerItem}>minutes</Text>
                  </View>
                  <View style={styles.pickerWrapper}>
                    <Picker
                      style={styles.picker}
                      selectedValue={selectedSeconds}
                      onValueChange={(itemValue) => setSelectedSeconds(itemValue)}
                    >
                      {AVAILABLE_SECONDS.map((value) => (
                        <Picker.Item key={value} label={value} value={value} />
                      ))}
                    </Picker>
                    <Text style={styles.pickerItem}>seconds</Text>
                  </View>
                </View>
                <View style={styles.modalButtonContainer}>
                  <TouchableOpacity onPress={handlePickerCancel} style={[styles.modalButton, styles.cancelButton]}>
                    <Text style={styles.buttonText}>Cancel</Text>
                  </TouchableOpacity>
                  <TouchableOpacity onPress={handlePickerConfirm} style={[styles.modalButton, styles.yesButton]}>
                    <Text style={styles.buttonText}>Confirm</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
          </View>
        </View>
      </Modal>
      <Modal
        transparent={true}
        visible={isTimerModalVisible}
        onRequestClose={() => {
          Alert.alert('Modal has been closed.');
          setTimerModalVisible(!isTimerModalVisible);
        }}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.timerModalContainer}>
            <Text style={styles.modalText}>Task</Text>
            <Text style={styles.modalTimer}>{formatTime(timer)}</Text>
            <View style={styles.buttonRow}>
              <TouchableOpacity onPress={() => { setTimerModalVisible(false); Alert.alert('Task Finished.'); }} style={[styles.modalButton, styles.finishedButton]}>
                <Text style={styles.buttonText}>Finished</Text>
              </TouchableOpacity>
            </View>
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
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  taskModalContainer: {
    backgroundColor: '#2B2B33',
    padding: 20,
    borderRadius: 10,
    width: '80%',
    alignItems: 'center',
  },
  taskText: {
    fontSize: 18,
    color: '#FFF',
    marginBottom: 20,
  },
  timerContainer: {
    backgroundColor: '#3E3E48',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 5,
    marginBottom: 20,
  },
  timerText: {
    fontSize: 24,
    color: '#FFF',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    width: '100%',
  },
  modalButtonContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  modalButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  moreTimeButton: {
    backgroundColor: '#5E5CE6',
    marginRight: 10,
  },
  yesButton: {
    backgroundColor: '#44CF6C',
    marginLeft: 10,
  },
  pickerWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 10,
  },
  buttonText: {
    fontSize: 16,
    color: '#FFF',
  },
  pickerContainer: { 
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
  },
  picker: {
    width: 80, 
    color: '#FFF',
    marginBottom: 10, 
  },
  pickerItem: {
    color: '#FFF',
    fontSize: 16,
  },
  timerModalContainer: {
    backgroundColor: '#2B2B33',
    padding: 20,
    borderRadius: 10,
    width: '80%',
    alignItems: 'center',
  },
  modalText: {
    fontSize: 18,
    color: '#FFF',
    marginBottom: 20,
  },
  modalTimer: {
    fontSize: 24,
    color: '#FFF',
    marginBottom: 20,
  },
  finishedButton: {
    position: 'relative',
    backgroundColor: '#44CF6C',
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#EF4444', 
    marginRight: 10,
  },
});

export default ChatScreen;
