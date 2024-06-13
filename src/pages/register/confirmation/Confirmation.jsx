import { useEffect, useRef, useState } from "react";
import logo from "../../../assets/logo.svg"
import style from "../register.module.scss"
import Input from "../../../components/Input";
import { Link,useNavigate } from "react-router-dom";

import axios from "axios";
import config from '../../../config.json'
function Confirmation(){
    const labels = [["Confirmation code",'number']];
    const [fields, setFields] = useState([''])
    const [pressed, setPressed] = useState([false])

    const [code, setCode] = useState("")
    function confirmHandler(){
        const url = `${config.url}/register/confirmation`;
        const EMAIL = localStorage.getItem('email')
        const data = {
            "code":+code,
            "email_address":EMAIL
        }
        axios.post(url,data).then(res=>console.log(res.data)).catch(err=>console.log(err))
    }
    function focusHandler(i){
        
        setPressed(prev=>{
            prev[i] = true
            return prev.slice(0)
        });
    }
    function resendHandler(){
        const url = `${config.url}/register/confirmation/resend?status=resend`
        
        axios.get(url).then(res=>console.log(res.data)).catch(err=>console.log(err))
    }
    function onClickOutsideHandler(i){
        if(fields[i].length==0 && pressed[i])setPressed(prev=>{prev[i]=false;return prev.slice(0);});
    }

    return(
        <div className={style.register}>
            <img src={logo} alt="" className={style.logo}/>

            <h1 className={style.title}>Get Started Now!</h1>
            <div className={style.create_text}>Create your account here</div>
            <div className={style.inputs}>
            <div className="confirmation">
                <input type="text" value={code} onChange={(e)=>setCode(e.target.value)}/>
                <button onClick={confirmHandler}>submit</button>
                <button onClick={resendHandler}>resend</button>
            </div>
            {
                labels.map((n,i)=>
                    <Input key={i} style={style} index={i} isAnimation={false} c={[fields,setFields]} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={()=>focusHandler(i)} onClickOutside={()=>onClickOutsideHandler(i)}/>
                )
            }
            </div>
            <div className={style.buttons}>
                
                
                
                <button className={style.login_btn} onClick={()=>{}}>
                        Login
                    </button>
                
                
            </div>
        </div>
    )
}
export default Confirmation;