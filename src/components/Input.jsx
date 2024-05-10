import React, { useRef, useEffect, useState } from 'react';
import eye_open from '../assets/eye_open.svg'
import eye_close from '../assets/eye_close.svg'


function Input(props) {
    const onClickOutside = props.onClickOutside
    const style = props.style
    const ref = useRef(null);
    const isPassword = props.inputType === "password"
    const [isHide, setIsHide] = useState(true);

    function passwordHandler() {
        setIsHide(!isHide)
    }
    useEffect(() => {

        const handleClickOutside = (event) => {
            if (ref.current && !ref.current.contains(event.target)) {
                onClickOutside();
            }
        };

        document.addEventListener('click', handleClickOutside);

        return () => {
            document.removeEventListener('click', handleClickOutside);
        };
    }, [onClickOutside]);

 

    return (
        <div className={`${style.input_wrapper} ${props.isAnimation?style.move_input:""}`} ref={ref} key={props.key}>
            <input className={`${style.input} ${isPassword?style.password:""}`} value={props.field[props.index]} type={isPassword ? isHide && "password" : "text"} onChange={(e) => { props.c[1](prev => { prev[props.index] = e.target.value; return prev.slice(0); }) }} onFocus={props.focusHandler} />
            <label htmlFor={style.input} className={`${style.placeholder} ${props.pressed[props.index] ? style.animation : ""}`}>{props.name}</label>
            {isPassword &&
                <div onClick={passwordHandler} className={style.password_btn}>
                        <img src={eye_open} className={isHide?style.hidden:""} style={{top:"2px"}} alt="" />
                        <img src={eye_close} className={!isHide?style.hidden:""} alt="" />                    
                </div>}
        </div>
    )
}

export default Input;