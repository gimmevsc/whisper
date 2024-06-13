import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.svg"
import style from "./register.module.scss"
import Input from "../../components/Input";
import { Link,useNavigate } from "react-router-dom";
import config from '../../config.json'
import axios from "axios";
function Register(){
    
    const navigate = useNavigate()
    const [isAnimation,setIsAnimation] = useState(false)
    const [pressed, setPressed] = useState([false,false,false])
    const [fields, setFields] = useState(['','',''])
    const labels = [["Email address",'text'],["Username",'text'],["Password",'password']];

    function registerHandler(){
        // const url = `http://${config.HOST}:${config.PORT}/register`
        const url = `${config.url}/register`

        const data = {
            'email_address':fields[0],
            'username':fields[1],
            'password':fields[2]
        }
        localStorage.setItem("email",data['email_address'])
        axios.post(url,data).then(res=>res.data).then(res=>console.log(res)).catch(err=>console.log(err));

        navigate("/register/confirmation")
    }
    function toLoginHandler(){
        setIsAnimation(true)
        setTimeout(() => {
            navigate("/login")
        }, 255);
    }
    function focusHandler(i){
        
        setPressed(prev=>{
            prev[i] = true
            return prev.slice(0)
        });
    }
    function onClickOutsideHandler(i){
        if(fields[i].length==0 && pressed[i])setPressed(prev=>{prev[i]=false;return prev.slice(0);});
    }
    useEffect(()=>{
        
    },[ fields,pressed])
    return(
        <div className={style.register}>
            <img src={logo} alt="" className={style.logo}/>

            <h1 className={style.title}>Get Started Now!</h1>
            <div className={style.create_text}>Create your account here</div>
            <div className={`${style.inputs} ${isAnimation?style.inputs_animation:""}`}>
            {
                labels.map((n,i)=>
                    <Input key={i} style={style} index={i} isAnimation={isAnimation && i==0} c={[fields,setFields]} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={()=>focusHandler(i)} onClickOutside={()=>onClickOutsideHandler(i)}/>
                )
            }
            </div>
            <div className={style.buttons}>
                <button className={`${style.register_btn} ${isAnimation?style.button_above:""}`} onClick={registerHandler}>
                    Register
                </button>
                <div className={style.text}>
                    Have an account?
                </div>
                
                
                <button className={`${style.login_btn} ${isAnimation?style.button_below:""}`} onClick={toLoginHandler}>
                        Login
                    </button>
                
                
            </div>
        </div>
    )
}

export default Register;