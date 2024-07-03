import React from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions } from 'react-native';
import Svg, { Line } from 'react-native-svg';

const TaskScreen = () => {
  const { width } = Dimensions.get('window');
  const circleSize = 40;
  const lineWidth = 2;

  const tasks = [
    {
      label: 'Task 1',
      color: '#D9D9D9',
      children: [
        { label: 'Task 2', color: '#FFD700' },
        { label: 'Task 3', color: '#6D8E72', children: [
          { label: 'Task 4', color: '#6D8E72' },
          { label: 'Task 5', color: '#6D8E72' },
          { label: 'Task 6', color: '#6D8E72' },
        ] },
      ],
    },
  ];

  const renderTasks = (tasks, parentY = 0, level = 0) => {
    const offsetX = width / 2;
    const verticalSpacing = 80; 

    return tasks.map((task, index) => {
      const currentY = parentY + (index + 1) * verticalSpacing;

      return (
        <View key={`${task.label}-${index}`} style={styles.taskContainer}>
          {level > 0 && (
            <Svg height={currentY} width="100%" style={styles.svg}>
              <Line
                x1={offsetX}
                y1={parentY}
                x2={offsetX}
                y2={currentY}
                stroke="#E4E4E4"
                strokeWidth={lineWidth}
                strokeDasharray="4"
              />
            </Svg>
          )}
          <View style={[styles.circle, { backgroundColor: task.color, left: offsetX - circleSize / 2, top: currentY }]}>
            <Text style={styles.taskText}>{task.label}</Text>
          </View>
          {task.children && renderTasks(task.children, currentY, level + 1)}
        </View>
      );
    });
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>This is a task</Text>
      </View>
      <View style={styles.timelineContainer}>
        {renderTasks(tasks)}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#202031',
    padding: 16,
  },
  header: {
    backgroundColor: '#FFD1D1',
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    textAlign: 'center',
  },
  timelineContainer: {
    position: 'relative',
    flex: 1,
  },
  svg: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  taskContainer: {
    position: 'relative',
    marginBottom: 24,
  },
  circle: {
    position: 'absolute',
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  taskText: {
    color: '#FFF',
    fontSize: 16,
  },
});

export default TaskScreen;
