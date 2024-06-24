import { useEffect, useRef, useState } from "react";
import style from "../reset.module.scss"
import Input from "../../../components/Input";
import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
import config from "../../../config.json"

function Second(props){
    const navigate = useNavigate()
    const [pressed, setPressed] = useState([false, false])
    const [isAnimation, setIsAnimation] = useState(false)
    const [fields, setFields] = useState(['', ''])
    const labels = [["Code", 'text'],["New password","password"]];

    function focusHandler(i) {

        setPressed(prev => {
            prev[i] = true
            return prev.slice(0)
        });
    }
    function sendHandler(){
            const url = `${config.url}/reset/confirmation`

            const data = {
                'email_address':localStorage.getItem("email"),
                'code':fields[0],
                'new_password':fields[1]
            }
            axios.post(url,data).then(res=>res.data).then(res=>{
                navigate('/login')
            }).catch(err=>console.log(err));
    }
    

    function onClickOutsideHandler(i) {
        if (fields[i].length == 0 && pressed[i]) setPressed(prev => { prev[i] = false; return prev.slice(0); });
    }
    useEffect(() => {
        
    }, [fields, pressed])
    return(
        <div className={style.block}>
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
                <a href="#">
                    <button className={style['cancel-btn']} onClick={()=>{props.setFirst(prev=>!prev)}}>Cancel</button>
                </a>
                <a href="#">
                    <button className={style['send-btn']} onClick={sendHandler}>Save</button>
                </a>
            </div>
        </div>
    )
}

export default Second;