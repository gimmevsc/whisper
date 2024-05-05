import React, { useRef, useEffect } from 'react';


function Input(props){
    const onClickOutside= props.onClickOutside
    const style  = props.style
    const ref = useRef(null);

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

    

    return(
            <div className={style.input_wrapper} ref={ref} key={props.key}>
                <input type="text" className={style.input} value={props.field[props.index]} onChange={(e)=>{props.c[1](prev=>{prev[props.index] =e.target.value;return prev.slice(0);})}} onFocus={props.focusHandler}/>
                <label htmlFor={style.input} className={`${style.placeholder} ${props.pressed[props.index]?style.animation:""}`}>{props.name}</label>
            </div>
    )
}

export default Input;