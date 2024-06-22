import { useEffect, useRef, useState } from "react";
import axios from "axios";
import avatar from "../../assets/logo.svg"
import { useParams } from "react-router-dom";
import Cookies from 'js-cookie';
import config from '../../config.json';
import ReconnectingWebSocket from 'reconnecting-websocket';
import style from "./chatroom.module.scss"
import decodeToken from "../../utils/decodeToken";
function ChatRoom() {
    const [messages, setMessages] = useState([]);
    const [sender,setSender] = useState("");
    const [receiver,setReceiver] = useState("");
    const [receiverUsername,setReceiverUsername] = useState("");
    const [senderUsername,setSenderUsername] = useState("");

    const [loaded, setLoaded] = useState(false)
    const messageInput = useRef();
    const [senderImg,setSenderImg] = useState(null);

    const [receiverImg,setReceiverImg] = useState(null);
    const {room} = useParams(); // Replace with dynamic room name as needed
    const messagesRef = useRef(null)
    const ws = useRef(null);
    useEffect(() => {
        const token = Cookies.get('token')
        console.log(token)
        const decoded = decodeToken(token);
        console.log(decoded)
        setSender(decoded.user_id)
        setSenderUsername(decoded.username)
        ws.current =new ReconnectingWebSocket(`${config.url.replace(/^http/, 'ws')}/ws/chat/${room}`);
        
        ws.current.onopen = () => {
            console.log('WebSocket connection established');
            if (!loaded){
                console.log(room)
    
                const url = `${config.url}/chat/${room}`
    
                const data = {
                    "receiver":room,
                    "sender_token" : Cookies.get('token')
                } 
                axios.post(url,data).then(res=>{
                    
                    setReceiver(res.data.receiver_id)
                    
                    setSenderImg(res.data.sender_avatar)
                    setReceiverUsername(res.data.receiver_username)
                    setReceiverImg(res.data.receiver_avatar);
                    setMessages(res.data.message)
                    setLoaded(true)
                }).then(()=>{
                    
                    scrollToBottom()

                }).catch(err=>console.log(err))
            }
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // console.log(event.data)
            setMessages(prevMessages => [...prevMessages, data]);
            scrollToBottom()

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
    const scrollToBottom = ()=>{
        setTimeout(() => {
            messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
        }, 1);
    }
    function sendMessageHandler(){
        console.log(messages)
        ws.current.send(messageInput.current.value)
        messageInput.current.value = ""
    }
    return (
        <div className={style["main"]}>
            
            <div className={style["chats"]}>
                <a href="/profile" className={style["top-bar"]}>
                    <img className={style["avatar"]} src={senderImg?`data:image/jpeg;base64,${senderImg}`:avatar} alt={senderUsername} />
                    <div className={style["text"]}>{senderUsername}</div>

                </a>
            </div>

            <div className={style["chat"]}>
                <div className="top-bar">
                    {receiverUsername}
                </div>
                <div className={style["bot"]}>
                <div className={style["messages"]} ref={messagesRef}>
                    {messages.map((msg, index) => (
                        <div key={index} className={style.message}>
                            <div className={style["message-data"]} style={msg.sender==sender ? {right:0}:{}}>
                                {msg.sender!=sender && <img className={style.avatar} src={receiverImg?`data:image/jpeg;base64,${receiverImg}`:avatar} alt={msg.username} />} 
                                <div className={style["text"]}>{msg.message}</div>
                            </div>
                            <div className={style["message-data"]} style={{opacity:0,position:"relative"}}>
                                {msg.sender!=sender && <img className={style.avatar} src={receiverImg?`data:image/jpeg;base64,${receiverImg}`:avatar} alt={msg.username} />} 
                                <div className={style["text"]}>{msg.message}</div>
                            </div>
                            
                        </div>
                    ))}
                </div>
                <div className={style['input-box']}>
                    <input className={style.input} type="text" ref={messageInput} onKeyDown={(e)=>{if(e.key =="Enter")sendMessageHandler()}} />
                    <button className={style["send-btn"]} onClick={sendMessageHandler}>Send</button>
                </div>
                </div>
                
            </div>
        </div>
    );
}

export default ChatRoom;
