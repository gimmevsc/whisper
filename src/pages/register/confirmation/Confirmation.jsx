import { useEffect, useRef, useState } from "react";
import logo from "../../../assets/logo.svg"
import style from "../register.module.scss"
import Input from "../../../components/Input";
import { Link, useNavigate } from "react-router-dom";

import axios from "axios";
import config from '../../../config.json'
function Confirmation() {
    const navigate = useNavigate()
    const labels = [["Confirmation code", 'number']];
    const [fields, setFields] = useState([''])
    const [pressed, setPressed] = useState([false])
    const [seconds,setSeconds] = useState(30)
    const isCounter = useRef(false)
    const interval = useRef(null)
    function confirmHandler() {
        const url = `${config.url}/register/confirmation`;
        const EMAIL = sessionStorage.getItem('email')
        const data = {
            "code": fields[0],
            "email_address": EMAIL
        }
        axios.post(url, data).then(res => {
            console.log(res.data)
            navigate('/login')
        }).catch(err => console.log(err))
    }
    function focusHandler(i) {

        setPressed(prev => {
            prev[i] = true
            return prev.slice(0)
        });
    }
    function resendHandler(seconds) {

        if(!isCounter.current){
            const url = `${config.url}/register/confirmation/resend?email_address=${sessionStorage.getItem("email")}`
            isCounter.current = true
            let temp = seconds
            interval.current = setInterval(() => {
                setSeconds(prevSeconds => prevSeconds - 1);
                temp--;
                console.log(temp)
                if(temp==0){
                    clearInterval(interval.current)
                    isCounter.current = false;
                    setSeconds(30);
                }
            }, 1000);
            axios.get(url).then(res => console.log(res.data)).catch(err => console.log(err))
        }
    }
    function onClickOutsideHandler(i) {
        if (fields[i].length == 0 && pressed[i]) setPressed(prev => { prev[i] = false; return prev.slice(0); });
    }

    useEffect(()=>{
        
        // Cleanup interval on component unmount
        return () => clearInterval(interval.current);
    },[])

    return (
        <div className={style.register}>
            <img src={logo} alt="" className={style.logo} />

            <h1 className={style.title}>Get Started Now!</h1>
            <div className={style.create_text}>Create your account here</div>
            <div className={style.inputs}>
                {
                    labels.map((n, i) =>
                        <Input key={i} style={style} index={i} isAnimation={false} c={[fields, setFields]} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={() => focusHandler(i)} onClickOutside={() => onClickOutsideHandler(i)} />
                    )
                }
            </div>
            <div className={style["button-container"]}>
                <div className={`${style['confirmation-buttons']}`}>
                    <button className={`${style['confirmation-resend-btn']} ${style['confirmation-btn']} ${isCounter.current? style['counter-btn']:""}`} onClick={()=>{resendHandler(seconds)}}>
                        {
                            isCounter.current? seconds: 'Resend'
                        }
                    </button>
                    <button className={`${style['confirmation-btn']} ${style['confirmation-submit-btn']}`} onClick={confirmHandler}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    )
}
export default Confirmation;