import React, { createContext, useState, useContext } from 'react';

const Context = createContext();

export const useUser = () => useContext(Context);

export const UserProvider = ({ children }) => {
  const [username, setUsername] = useState('');

  // Currently not used
  return (
    <Context.Provider value={[ username, setUsername ]}>
      {children}
    </Context.Provider>
  );
};
