import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import Cookies from 'js-cookie';
import config from '../../config.json';
import ReconnectingWebSocket from 'reconnecting-websocket';

function ChatRoom() {
    const [messages, setMessages] = useState([]);
    const messageInput = useRef();
    const {room} = useParams(); // Replace with dynamic room name as needed
    const ws = useRef(null);
    useEffect(() => {
        console.log(room)
        const url = `${config.url}/chat/${room}`

        const data = {
            "receiver":room,
            "sender_token" : Cookies.get('token')
        } 
        axios.post(url,data).then(res=>{
            console.log("Load the page")
            // console.log(res.data)
        }).catch(err=>console.log("what"))
        ws.current =new ReconnectingWebSocket(`${config.url.replace(/^http/, 'ws')}/ws/chat/${room}`);
        // Fetch initial chat messages
        

               

        // Set up WebSocket for real-time updates
        

        ws.current.onopen = () => {
            console.log('WebSocket connection established');
            
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(event.data)
            setMessages(prevMessages => [...prevMessages, data]);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };

        ws.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        // Clean up the WebSocket connection when the component is unmounted
        return () => {
            ws.current.close();
        };
    }, []);
    function sendMessageHandler(){
        console.log(messages)
        ws.current.send(messageInput.current.value)
    }
    return (
        <div className="main">
            
            <div className="chats">
                chats
            </div>

            <div className="chat">
                <div className="top-bar">
                    Username
                </div>
                <div className="messages">
                    {messages.map((msg, index) => (
                        <div key={index}>
                            <strong>{msg.username}:</strong> {msg.message}
                        </div>
                    ))}
                </div>

                <input type="text" ref={messageInput} onChange={() => console.log(messageInput.current.value)} />
                <button onClick={sendMessageHandler}>Click</button>
            </div>
        </div>
    );
}

export default ChatRoom;
