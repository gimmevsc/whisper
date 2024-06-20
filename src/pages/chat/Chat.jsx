import { useEffect, useRef, useState } from "react";
import axios from "axios";

import Cookies from 'js-cookie';
import config from '../../config.json';
import ReconnectingWebSocket from 'reconnecting-websocket';

function Chat() {
    const [messages, setMessages] = useState([]);
    const messageInput = useRef();
    const roomName = '17'; // Replace with dynamic room name as needed
    let ws;
    useEffect(() => {
        // Fetch initial chat messages
        const url = `${config.url}/chat/${roomName}`

        const data = {
            "lol":"hello",
            "token" : Cookies.get('token')
        }        

        // Set up WebSocket for real-time updates
        ws = new ReconnectingWebSocket(`${config.url.replace(/^http/, 'ws')}/ws/chat/${roomName}/`);

        ws.onopen = () => {
            console.log('WebSocket connection established');
            axios.post(url,data).then(res=>{
                console.log("hello")
                // console.log(res.data)
            }).catch(err=>console.log("what"))
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages(prevMessages => [...prevMessages, data.message]);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        // Clean up the WebSocket connection when the component is unmounted
        return () => {
            ws.close();
        };
    }, []);

    return (
        <div className="main">
            <div className="header">
                {/* Add any header content here */}
            </div>

            <div className="chats">
                {/* Add any chat list content here */}
            </div>

            <div className="chat">
                <div className="messages">
                    {messages.map((msg, index) => (
                        <div key={index}>
                            <strong>{msg.sender}:</strong> {msg.message} <em>({new Date(msg.timestamp).toLocaleString()})</em>
                        </div>
                    ))}
                </div>

                <input type="text" ref={messageInput} onChange={() => console.log(messageInput.current.value)} />
                <button onClick={()=>{ws.send(messageInput.current.value)}}>Click</button>
            </div>
        </div>
    );
}

export default Chat;
