import { useEffect, useRef, useState } from "react";
import style from "../reset.module.scss"
import Input from "../../../components/Input";
import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
import config from "../../../config.json"

function First(props){
    const navigate = useNavigate()
    const [pressed, setPressed] = useState([false, false, false])
    const [isAnimation, setIsAnimation] = useState(false)
    const [fields, setFields] = useState([''])
    const labels = [["Email", 'email']];
    const isValidEmail = (email) => {
        // Simple regex for email validation
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };
    function focusHandler(i) {


        setPressed(prev => {
            prev[i] = true
            return prev.slice(0)
        });
    }
    const emailHandler = ()=>{
        const email = fields[0];
        if(isValidEmail(email)){
            const url = `${config.url}/reset`

            const data = {
                'email_address':fields[0],
            }
            localStorage.setItem("email",data['email_address'])
            let s = Date.now()
            axios.post(url,data).then(res=>{
                props.setFirst(prev=>!prev);
                console.log(Date.now() - s )
            }).catch(err=>{
                alert("non valid email")
                console.log(err.response.data.type)
            });
            

        }else{
            alert("non valid email")
        }

    }
    
    function onClickOutsideHandler(i) {
        if (fields[i].length == 0 && pressed[i]) setPressed(prev => { prev[i] = false; return prev.slice(0); });
    }
    useEffect(() => {
        
    }, [fields, pressed])
    return(
        <div  className={style.block}>
        <div className={style.create_text}>Enter your email address to receive a password reset code</div>
            <div className={style.inputs}>
                {
                    labels.map((n, i) =>
                        <Input key={i} style={style} index={i} c={[fields, setFields]} isAnimation={isAnimation && i==1} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={() => focusHandler(i)} onClickOutside={() => onClickOutsideHandler(i)} />
                    )
                }
                
                
            </div>
            <div className={style["check-box"]}>
            </div>
            <div className={`${style.buttons}`}>
                <a href="/login">
                    <button className={style['cancel-btn']}>Cancel</button>
                </a>
                <a href="#">
                    <button className={style['send-btn']} onClick={emailHandler}>Send</button>
                </a>
            </div>
        </div>
    )
}

export default First;