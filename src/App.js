import './App.css';
import Register from './pages/register/Register';
import Login from './pages/login/Login';
import Reset from './pages/reset/Reset';
import Chat from './pages/chat/Chat';
import ChatRoom from './pages/chatroom/ChatRoom';
import Profile from './pages/profile/Profile'
import Confirmation from './pages/register/confirmation/Confirmation';
import { BrowserRouter, Routes, Route } from "react-router-dom";
function App() {
  return (
    <BrowserRouter>
      <Routes>
      
        <Route path="/" element={<Login />}/>
        <Route path="/login" element={<Login />}/>
        <Route path="/register" element={<Register />}/>
        <Route path="/register/confirmation" element={<Confirmation />}/>
        <Route path="/reset" element={<Reset />}/>
        <Route path="/chatroom/:room" element={<ChatRoom />}/>
        <Route path="/chat" element={<Chat />}/>
        <Route path="/profile" element={<Profile />}/>


          {/* <Route index element={<Home />} />
          <Route path="blogs" element={<Blogs />} />
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<NoPage />} /> */}
        
      </Routes>
    </BrowserRouter>
    
  );
}

export default App;
