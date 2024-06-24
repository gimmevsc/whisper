import { useEffect, useRef, useState } from "react";
import axios from "axios";
import avatar from "../../assets/logo.svg"
import { useParams, useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import config from '../../config.json';
import ReconnectingWebSocket from 'reconnecting-websocket';
import style from "./chatroom.module.scss"
import decodeToken from "../../utils/decodeToken";
import ChatComponent from "./chatComponent/ChatComponent";
function ChatRoom() {
    const navigate = useNavigate()

    const [messages, setMessages] = useState([]);
    // const [sender, setSender] = useState("");
    const sender = useRef('');
    const [receiver, setReceiver] = useState("");
    const [receiverUsername, setReceiverUsername] = useState("");
    // const [senderUsername, setSenderUsername] = useState("");
    const senderUsername = useRef('')
    const [searchUsers, setSearchUsers] = useState([])
    const [search, setSearch] = useState('')
    // const [loaded, setLoaded] = useState(false)
    const loaded = useRef(false)
    const [userChats, setUserChats] = useState([])
    const messageInput = useRef();
    const [senderImg, setSenderImg] = useState(null);
    const [receiverImg, setReceiverImg] = useState(null);
    const { room } = useParams(); // Replace with dynamic room name as needed
    const messagesRef = useRef(null)
    const ws = useRef(null);
    const getChats = () => { 
        const URL = `${config.url}/userchats?user_id=${sender.current}`

        axios.get(URL).then((res) => {
            setUserChats([{"user_id":sender.current,'profile_picture':senderImg,'username':"SAVED MESSAGES"},...res.data])
            console.log("chats received")
            console.log(res.data)
        }).catch(err => {
            // setUserChats([])
            console.log(err)
        })
    }
    const chatHandler = () => {
        const url = `${config.url}/chat/${room}`

        const data = {
            "receiver": room,
            // "user_id": sender
            "user_id": sender.current

        }
        axios.post(url, data).then(res => {

            setReceiver(res.data.receiver_id)

            setSenderImg(res.data.sender_avatar)
            setReceiverUsername(res.data.receiver_username)
            setReceiverImg(res.data.receiver_avatar);
            setMessages(res.data.message)
            console.log('Chat is loaded')
            console.log(res.data)

        }).then(() => {
            scrollToBottom()
        }).catch(err => console.log(err))
    }
    const wsHandler = () => {
        ws.current = new ReconnectingWebSocket(`${config.url.replace(/^http/, 'ws')}/ws/chat/${room}`);

        ws.current.onopen = () => {
            console.log('WebSocket connection established');
            chatHandler()

        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages(prevMessages => [...prevMessages, data]);
            scrollToBottom()
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };

        ws.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }


    useEffect(() => {
        console.log("useEffect")
        if(!loaded.current){
            console.log("loading first time")
            const token = Cookies.get('token')
            const decoded = decodeToken(token);
            console.log(decoded)
            sender.current = decoded.user_id
            
            senderUsername.current = decoded.username
            getChats()
            
        }
        
        
    
        wsHandler()
    
        
        
        // setLoaded(true)
        loaded.current = true;
        
        return () => {
            ws.current.close();
        };
    }, [room]);
    const scrollToBottom = () => {
        setTimeout(() => {
            messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
        }, 1);
    }
    function sendMessageHandler() {
        console.log(messages)
        ws.current.send(messageInput.current.value)
        messageInput.current.value = ""
    }
    function searchHandler(event) {
        setSearch(event.target.value)
        const URL = `${config.url}/search?username=${event.target.value}&user_id=${sender.current}`;
        if (event.target.value !== "") {
            axios.get(URL).then(res => {
                console.log(res.data)
                setSearchUsers(res.data)
            }).catch(err => {
                setSearchUsers([])
            })
        } else {
            setSearchUsers([])
        }
    }
    const logoutHandler = ()=>{
        Cookies.remove('token')
        navigate('/login')
    }
    return (
        <div className={style["main"]}>

            <div className={style["chats"]}>
                <div className={style["top-bar"]}>
                    <a href="/profile" className={style["profile"]}>
                        <img className={style["avatar"]} src={senderImg ? `data:image/jpeg;base64,${senderImg}` : avatar} alt={senderUsername.current} />
                        <div className={style["text"]}>{senderUsername.current}</div>

                    </a>
                    <div className={style["search"]}>
                        <input type="text" className={style['search-bar']} value={search} onChange={searchHandler} />
                        <div className={style["search-users"]}>
                            {
                                searchUsers.map((user,i) =>
                                    <div className={`${style["search-item"]}`} key={i}>
                                        <div className={style["user-avatar"]}>
                                            <img src={user.profile_picture ? `data:image/jpeg;base64,${user.profile_picture}` : avatar} alt={user.username} />
                                        </div>
                                        <div className={style["username"]}>
                                            {user.username}
                                        </div>
                                        <button className={style["message"]} onClick={() => { navigate(`/chatroom/${user.user_id}`) }}>
                                            Message
                                        </button>
                                    </div>
                                )
                            }
                        </div>
                    </div>
                </div>
                <div className={style["chats-box"]}>
                        {
                            userChats.map((chat,i)=>
                                <div key={i} className={`${style["chat"]} ${chat.user_id==room?style.active:""}`} onClick={()=>{navigate(`/chatroom/${chat.user_id}`)}}>
                                    <div className={style["user-avatar"]}>
                                        <img src={chat.profile_picture ? `data:image/jpeg;base64,${chat.profile_picture}` : avatar} alt="" />
                                    </div>
                                    <div className="username">
                                        {chat.username}
                                    </div>
                                </div>
                            )
                        }
                </div>
                <div className="logout">
                    <button onClick={logoutHandler}>Log out</button>
                </div>
            </div> 

            <ChatComponent messages={messages}
                           style={style}
                           receiverImg={receiverImg}
                           receiverUsername={receiverUsername}
                           messagesRef={messagesRef}
                           sender={sender}
                           messageInput={messageInput}
                           sendMessageHandler={sendMessageHandler} 
                           room={room}
            />
        </div>
    );
}

export default ChatRoom;
