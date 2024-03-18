import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter, Routes, Route  } from 'react-router-dom';
import Main from './sitePagesRouting/main'
import SignUp from './sitePagesRouting/signUp'
import LogIn from './sitePagesRouting/logIn'
import Request from './sitePagesRouting/request'


function App() {
  
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<Main /> } />
          <Route path="/signUp" element={<SignUp />} />
          <Route path="/logIn" element={<LogIn />} />
          <Route path="request" element={<Request />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
