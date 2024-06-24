import { useEffect, useRef, useState } from "react";
import Cookies from 'js-cookie';
import logo from "../../assets/logo.svg"
import style from "./login.module.scss"
import Input from "../../components/Input";
import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
import config from "../../config.json"
import decodeToken from '../../utils/decodeToken'
function Login() {
    
    const navigate = useNavigate()
    const [pressed, setPressed] = useState([false, false, false])
    const [isAnimation, setIsAnimation] = useState(false)
    const [fields, setFields] = useState(['', ''])
    const labels = [["Username or email", 'text'], ["Password", 'password']];
    const [error,setError] = useState('')
    function focusHandler(i) {

        setPressed(prev => {
            prev[i] = true
            return prev.slice(0)
        });
    }

    function loginHandler(){
        // const url = `http://${config.HOST}:${config.PORT}`
        const url = `${config.url}/login`

        const data = {
            "username":fields[0],
            "password":fields[1]
        }
        axios.post(url,data).then(res=>{
            Cookies.set('token', res.data.token); // Expires in 30 days
            
            const id = decodeToken(Cookies.get('token')).user_id
            navigate(`/chatroom/${id}`)
        }).catch(err=>{
            console.log(err.response.data.message)
            setError(err.response.data.message)

        })
    }
 
    function toRegisterHandler(){
        setIsAnimation(true)
        setTimeout(() => {
            navigate("/register")
        }, 255);
    }

    function onClickOutsideHandler(i) {
        if (fields[i].length == 0 && pressed[i]) setPressed(prev => { prev[i] = false; return prev.slice(0); });
    }
    useEffect(() => {
        
    }, [fields, pressed])
    return (
        <div className={style.login}>
            <img src={logo} alt="" className={style.logo} />

            <h1 className={style.title}>Welcome back!</h1>
            <div className={style.create_text}>Create an account or Log in</div>
            <div className={style.inputs} onKeyDown={(e)=>{if(e.key==="Enter")loginHandler()}}>
                {
                    labels.map((n, i) =>
                        <Input key={i} style={style} index={i} c={[fields, setFields]} isAnimation={isAnimation && i==1} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={() => focusHandler(i)} onClickOutside={() => onClickOutsideHandler(i)} />
                    )
                }
                <div className={`${style.input_wrapper} ${style.animation_input} ${isAnimation?style.opacity_input:""}`} >
                    <input type="text" placeholder="Username" className={style.input} />
                </div>
                
                <div className={`${style.forgot_password} ${isAnimation?style.forgot_password_animation:""}`}>
                    <a href="/reset">Forgot your password?</a>
                    
                </div>
                <div className={style["errors"]}>
                    {error}
                </div>
            </div>
            <div className={`${style.buttons} ${isAnimation?style.buttons_animation:""}`}>
                <button className={`${style.register_btn} ${isAnimation?style.button_above:""}`} onClick={loginHandler}>
                    Login
                </button>
                <div className={style.text}>
                    Don’t have an account?
                </div>
                
                    <button className={`${style.login_btn} ${isAnimation?style.button_below:""}`} onClick={toRegisterHandler}>
                        Register
                    </button>

                
            </div>
        </div>
    )
}

export default Login;