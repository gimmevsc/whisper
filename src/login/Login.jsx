import { useEffect, useRef, useState } from "react";
import logo from "../assets/logo.svg"
import style from "./login.module.scss"
import Input from "./Input";
function Login(){
    const [pressed, setPressed] = useState([false,false,false])
    const [fields, setFields] = useState(['','',''])
    const labels = ["Email address","Username","Password"];

    function inputChange(e, i){
        console.log(i)
        setFields(prev=>{
            prev[i] = e.target.value
            console.log(prev)
            return prev.slice(0)
        });
        // if(e.target.value.length ==0 && pressed )setPressed(false)
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
        <div className={style.login}>
            <img src={logo} alt="" className={style.logo}/>

            <h1 className={style.title}>Get Started Now!</h1>
            <div className={style.create_text}>Create your account here</div>
            {
                labels.map((n,i)=>
                    <Input key={i} style={style} index={i} c={[fields,setFields]} field={fields} pressed={pressed} name={n} focusHandler={()=>focusHandler(i)} onClickOutside={()=>onClickOutsideHandler(i)}/>
                )
            }
            <div className={style.buttons}>

            </div>
        </div>
    )
}

export default Login;