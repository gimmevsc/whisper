import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.svg"
import style from "./login.module.scss"
import Input from "../../components/Input";
import { Link,useNavigate } from "react-router-dom";
function Login() {
    const navigate = useNavigate()
    const [pressed, setPressed] = useState([false, false, false])
    const [isAnimation, setIsAnimation] = useState(false)
    const [fields, setFields] = useState(['', ''])
    const labels = [["Username or email", 'text'], ["Password", 'password']];

    function focusHandler(i) {

        setPressed(prev => {
            prev[i] = true
            return prev.slice(0)
        });
        console.log(pressed)
    }

    function toRegisterHandler(){
        setIsAnimation(true)
        setTimeout(() => {
            navigate("/register")
        }, 250);
    }

    function onClickOutsideHandler(i) {
        if (fields[i].length == 0 && pressed[i]) setPressed(prev => { prev[i] = false; return prev.slice(0); });
    }
    useEffect(() => {
        console.log(fields[0])
    }, [fields, pressed])
    return (
        <div className={style.login}>
            <img src={logo} alt="" className={style.logo} />

            <h1 className={style.title}>Welcome back!</h1>
            <div className={style.create_text}>Create an account or Log in</div>
            <div className={style.inputs}>
                {
                    labels.map((n, i) =>
                        <Input key={i} style={style} index={i} c={[fields, setFields]} field={fields} pressed={pressed} name={n[0]} inputType={n[1]} focusHandler={() => focusHandler(i)} onClickOutside={() => onClickOutsideHandler(i)} />
                    )
                }
                <div className={style.forgot_password}>
                    Forgot your password?
                </div>
            </div>
            <div className={`${style.buttons} ${isAnimation&&style.buttons_animation}`}>
                <button className={`${style.register_btn} ${isAnimation&&style.button_above}`}>
                    Login
                </button>
                <div className={style.text}>
                    Don’t have an account?
                </div>
                
                    <button className={`${style.login_btn} ${isAnimation&&style.button_below}`} onClick={toRegisterHandler}>
                        Register
                    </button>

                
            </div>
        </div>
    )
}

export default Login;