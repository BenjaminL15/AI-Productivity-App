import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, Animated, TouchableOpacity } from 'react-native';

const family = [
  {
    id: 'Writing Emails',
    name: 'Writing Emails',
    children: [
      {
        id: 'Gather Emails',
        name: 'Gather Emails',
        children: [
          {
            id: 'Send',
            name: 'Send Emails',
          },
        ],
      },
    ],
  },
  {
    id: 'Plan a Party',
    name: 'Plan a Party',
    children: [
      {
        id: 'Gather the invitees',
        name: 'Gather the invitees',
        children: [
          {
            id: 'Send invites',
            name: 'Send invites',
          },
        ],
      },
    ],
  },
];

const Node = ({ node, level, isExpanded, onToggle, expandedChild, setExpandedChild }) => {
  const [height] = useState(new Animated.Value(isExpanded ? 70 : 0));
  const [lineOpacity] = useState(new Animated.Value(isExpanded ? 1 : 0));

  useEffect(() => {
    Animated.parallel([
      Animated.timing(height, {
        toValue: isExpanded ? 70 : 0,
        duration: 300,
        useNativeDriver: false,
      }),
      Animated.timing(lineOpacity, {
        toValue: isExpanded ? 1 : 0,
        duration: 300,
        useNativeDriver: false,
      }),
    ]).start();
  }, [isExpanded]);

  const hasChildren = node.children && node.children.length > 0;

  const handlePress = () => {
    if (hasChildren) {
      if (expandedChild === node.id) {
        setExpandedChild(null);
      } else {
        setExpandedChild(node.id);
      }
      onToggle(node.id);
    }
  };

  return (
    <View style={styles.nodeContainer}>
      <TouchableOpacity onPress={handlePress} disabled={!hasChildren} style={{ flexDirection: 'row', alignItems: 'center' }}>
        <View style={styles.circle(level)} />
        <Text style={[styles.text, { marginLeft: 20, color: hasChildren ? '#ffffff' : '#666666' }]}>
          {node.name}
        </Text>
      </TouchableOpacity>
      {hasChildren && (
        <Animated.View
          style={[
            styles.line,
            { marginLeft: 35 * (level + 1) - 15, height, opacity: lineOpacity },
          ]}
        />
      )}
      {isExpanded && hasChildren && node.children.slice(0, 1).map(childNode => (
        <Node
          key={childNode.id}
          node={childNode}
          level={level + 1}
          isExpanded={expandedChild === childNode.id}
          onToggle={onToggle}
          expandedChild={expandedChild}
          setExpandedChild={setExpandedChild}
        />
      ))}
      {hasChildren && node.children.slice(1).map(childNode => (
        <View key={childNode.id} style={styles.nodeContainer}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <View style={styles.circle(level + 1)} />
            <Text style={[styles.text, { marginLeft: 20, color: '#666666' }]}>
              {childNode.name}
            </Text>
          </View>
          <Animated.View
            style={[
              styles.line,
              { marginLeft: 35 * (level + 2) - 15, height: 70, opacity: lineOpacity },
            ]}
          />
        </View>
      ))}
    </View>
  );
};

const App = () => {
  const [expandedNodes, setExpandedNodes] = useState({});
  const [expandedChild, setExpandedChild] = useState(null);

  const handleToggle = (nodeId) => {
    setExpandedNodes(prevState => ({
      ...prevState,
      [nodeId]: !prevState[nodeId],
    }));
  };

  return (
    <View style={styles.container}>
      <View style={styles.taskBox}>
        <Text style={styles.taskBoxText}>This is a task</Text>
      </View>
      {family.map((node, index) => (
        <Node
          key={node.id}
          node={node}
          level={0}
          isExpanded={!!expandedNodes[node.id]}
          onToggle={handleToggle}
          expandedChild={expandedChild}
          setExpandedChild={setExpandedChild}
        />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1c1c2b',
    paddingHorizontal: 20,
    paddingVertical: 40,
  },
  taskBox: {
    backgroundColor: '#ffcccc',
    padding: 30,
    borderRadius: 20,
    marginBottom: 40,
  },
  taskBoxText: {
    color: '#000',
    fontSize: 24,
    textAlign: 'center',
  },
  nodeContainer: {
    flexDirection: 'column',
    marginBottom: 40,
  },
  circle: (level) => ({
    width: level === 0 ? 50 : 40,
    height: level === 0 ? 50 : 40,
    borderRadius: level === 0 ? 25 : 20,
    backgroundColor: level === 0 ? '#ffd700' : '#cd853f',
  }),
  text: {
    fontSize: 20,
  },
  line: {
    width: 2,
    backgroundColor: '#ffffff',
    alignSelf: 'flex-start',
  },
});

export default App;