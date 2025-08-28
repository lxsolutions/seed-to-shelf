import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';

export default function ChefApp() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chef Dashboard</Text>
      <Text style={styles.subtitle}>Manage your kitchen and orders</Text>

      <Button
        title="Accept Orders"
        onPress={() => alert('Order acceptance coming soon!')}
        color="#4CAF50"
      />

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
    paddingHorizontal: 20,
  },
});
