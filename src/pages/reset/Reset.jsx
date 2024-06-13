import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.svg"
import style from "./reset.module.scss"
import Input from "../../components/Input";
import First from "./first/First"
import Second from "./second/Second"

import { Link,useNavigate } from "react-router-dom";
import axios from "axios";
import config from "../../config.json"
function Reset(){
    
    const [isFirst,setFirst] = useState(true);
    
    

    return(
        <div className={style.reset}>
            <img src={logo} alt="" className={style.logo} />

            <h1 className={style.title}>Reset your password</h1>
            {isFirst?
                    <First setFirst={setFirst}/>:
                    <Second setFirst={setFirst}/>}
            
            

        </div>

    )
}

export default Reset;