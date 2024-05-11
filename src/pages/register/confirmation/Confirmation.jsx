import axios from "axios";
import config from '../../../config.json'
import { useState } from "react";
function Confirmation(){
    const [code, setCode] = useState("")
    function confirmHandler(){
        const url = `${config.url}/register/confirmation`
        const data = {
            "code":+code
        }
        axios.post(url,data).then(res=>console.log(res.data)).catch(err=>console.log(err))
    }
    function resendHandler(){
        const url = `${config.url}/register/confirmation/resend?status=resend`
        
        axios.get(url).then(res=>console.log(res.data)).catch(err=>console.log(err))
    }
    return(
        <div className="confirmation">
            <input type="text" value={code} onChange={(e)=>setCode(e.target.value)}/>
            <button onClick={confirmHandler}>submit</button>
            <button onClick={resendHandler}>resend</button>
        </div>
    )
}
export default Confirmation;