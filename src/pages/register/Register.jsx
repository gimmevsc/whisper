import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.svg"
import style from "./register.module.scss"
import Input from "../../components/Input";
import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
function Register(){
    const HOST = "127.0.0.1"
    const navigate = useNavigate()
    const [isAnimation,setIsAnimation] = useState(false)
    const [pressed, setPressed] = useState([false,false,false])
    const [fields, setFields] = useState(['','',''])
    const labels = [["Email address",'text'],["Username",'text'],["Password",'password']];

    function registerHandler(){
        // const data = {
        //     'email':fields[0],
        //     'username':fields[1],
        //     'password':fields[2]
        // }
        axios.get(`http://${HOST}:8000/register?email_address=${fields[0]}&username=${fields[1]}&password=${fields[2]}`).then(res=>res.data).then(res=>console.log(res)).catch(err=>console.log(err))
    }
    function toRegisterHandler(){
        setIsAnimation(true)
        setTimeout(() => {
            navigate("/login")
        }, 250);
    }
    function focusHandler(i){
        
        setPressed(prev=>{
            prev[i] = true
            return prev.slice(0)
        });
        console.log(pressed)
    }
    function onClickOutsideHandler(i){
        if(fields[i].length==0 && pressed[i])setPressed(prev=>{prev[i]=false;return prev.slice(0);});
    }
    useEffect(()=>{
        console.log(fields[0])
    },[ fields,pressed])
    return(
        <div className={style.register}>
            <img src={logo} alt="" className={style.logo}/>

            <h1 className={style.title}>Get Started Now!</h1>
            <div className={style.create_text}>Create your account here</div>
            {
                labels.map((n,i)=>
                    <Input key={i} style={style} index={i} c={[fields,setFields]} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={()=>focusHandler(i)} onClickOutside={()=>onClickOutsideHandler(i)}/>
                )
            }
            <div className={style.buttons}>
                <button className={`${style.register_btn} ${isAnimation&&style.button_above}`} onClick={registerHandler}>
                    Register
                </button>
                <div className={style.text}>
                    Have an account?
                </div>
                
                
                <button className={`${style.login_btn} ${isAnimation&&style.button_below}`} onClick={toRegisterHandler}>
                        Login
                    </button>
                
                
            </div>
        </div>
    )
}

export default Register;