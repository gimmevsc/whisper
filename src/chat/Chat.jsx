import { useEffect, useRef, useState } from "react";
import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
import config from '../config.json'
import Cookies from 'js-cookie';
import ReconnectingWebSocket from 'reconnecting-websocket';

function Chat(){
    const [messages,setMessages] = useState();
    const message = useRef();   


    useEffect(()=>{
        console.log("hello)")
        const ws = new ReconnectingWebSocket( config.url+'/ws/chatroom/chat' );

        ws.onopen = () => {
            console.log('WebSocket connection established');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);

            setMessages(data.message);
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


    },[])
    return(
        <div className="main">
            <div className="header">

            </div>

            <div className="chats">

            </div>
            <div className="chat">

                <div className="messages">

                </div>

                <input type="text" ref={message} onChange={()=>{console.log(message.current)}}/>

            </div>
        </div>

    )
}
export default Chat;