

import { useEffect } from "react";
import avatar from "../../../assets/logo.svg"

function ChatComponent({messages,style,receiverImg,receiverUsername,messagesRef,sender,messageInput,sendMessageHandler,room}){

    useEffect(()=>{

    },[room])
    return (
        <div className={style["chat"]}>
                <div className="top-bar">
                    {receiverUsername}
                </div>
                <div className={style["bot"]}>
                    <div className={style["messages"]} ref={messagesRef}>
                        {messages.map((msg, index) => (
                            <div key={index} className={style.message}>
                                <div className={style["message-data"]} style={msg.sender === sender.current ? { right: 0 } : {}}>
                                    {msg.sender !== sender.current && <img className={style.avatar} src={receiverImg ? `data:image/jpeg;base64,${receiverImg}` : avatar} alt={msg.username} />}
                                    <div className={style["text"]}>{msg.message}</div>
                                </div>
                                <div className={style["message-data"]} style={{ opacity: 0, position: "relative" }}>
                                    {msg.sender !== sender.current && <img className={style.avatar} src={receiverImg ? `data:image/jpeg;base64,${receiverImg}` : avatar} alt={msg.username} />}
                                    <div className={style["text"]}>{msg.message}</div>
                                </div>

                            </div>
                        ))}
                    </div>
                    <div className={style['input-box']}>
                        <input className={style.input} type="text" ref={messageInput} onKeyDown={(e) => { if (e.key === "Enter") sendMessageHandler() }} />
                        <button className={style["send-btn"]} onClick={sendMessageHandler}>Send</button>
                    </div>
                </div>

            </div>
    )
}

export default ChatComponent;